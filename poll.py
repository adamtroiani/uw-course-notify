from __future__ import annotations

import datetime as dt
import asyncio
from collections import defaultdict
from typing import Dict, Set, Tuple, List

from sqlalchemy import select, update
from sqlalchemy.orm import Session, sessionmaker

from database import engine
from models.subscriber import Subscriber
from check_availability import check_availability

from exponent_server_sdk import PushClient, PushMessage, PushServerError

import logging
from logging_config import init_logging

init_logging()

# --- config ---
POLL_SECONDS = 60
NOTIFICATION_FREQUENCY_MINS = 5 
ANDROID_CHANNEL_ID = "default"
IOS_INTERRUPTION_LEVEL = "time-sensitive"
# ---------------

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

logger = logging.getLogger(__name__)
client = PushClient()

def load_subscriptions(db: Session) -> Dict[Tuple[str, int], Set[str]]:
    tokens_by_key: Dict[Tuple[str, int], Set[str]] = defaultdict(set)
    cutoff = dt.datetime.utcnow() - dt.timedelta(minutes=5)
    
    rows = db.execute(
        select(Subscriber.course, Subscriber.term, Subscriber.token)
        .distinct()
        .where(
            (Subscriber.last_notified == None) |
            (Subscriber.last_notified < cutoff)
        )
    ).all()
    for course, term, token in rows:
        tokens_by_key[(course, term)].add(token)
        
    return tokens_by_key


def notify_group(
    course: str, term: int, tokens: Set[str], open_sections: List[str], db: Session
) -> None:
    title = f"🚨 {course} has an open spot!"
    body = f'Opening{"s" if len(open_sections) > 1 else ""}: {"\n".join(open_sections)}'

    for token in tokens:
        logger.info(f"notifying {token} for {course} during term {term}")
        message = PushMessage(
            to=token,
            sound="default",
            title=title,
            body=body,
            priority="high",
            data={"course": course, "available_sections": open_sections},
        )

        try:
            resp = client.publish(message)
        except PushServerError as exc:
            logger.exception(f"PushServerError: {exc}")
        except Exception as exc:
            logger.exception(f"Unknown error: {exc}")
    
    if tokens:
        db.execute(
            update(Subscriber)
            .where(
                Subscriber.course == course,
                Subscriber.term == term,
                Subscriber.token.in_(tokens)
            )
            .values(last_notified=dt.datetime.utcnow())
        )
        db.commit()

async def poll_once() -> None:
    with SessionLocal() as db:
        subs = load_subscriptions(db)
        if not subs:
            logger.info("No subscribers yet.")
            return

        for (course, term), tokens in subs.items():
            try:
                sections = check_availability(course, term)
                
                if sections:
                    logger.info(f"{course} openings:")
                    for section in sections:
                        logger.info(f"  {section}")
                else:
                    logger.info(f"{course} is full.")
            except Exception:
                logger.exception("check_availability failed for %s / %s", course, term)
                continue

            if sections:
                notify_group(course, term, tokens, sections, db)


async def main() -> None:
    while True:
        try:
            await poll_once()
        except Exception:
            logger.exception("Poll loop error")
        await asyncio.sleep(POLL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
