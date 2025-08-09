from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from exponent_server_sdk import PushClient, PushMessage, PushServerError
import uvicorn
from check_availability import check_availability
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import init_db
from models import Subscriber
from deps import get_db

import logging
from logging_config import init_logging

init_logging()

logger = logging.getLogger(__name__)
push_client = PushClient()


class Sub(BaseModel):
    course: str
    push_token: str
    term: int


def build_app() -> FastAPI:
    app = FastAPI(
        title="UW Notify API",
        version="0.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # dev only
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/availability/{course}/{term}")
    async def availability(course: str, term: int, background_tasks: BackgroundTasks):
        available_sections = check_availability(course, term)

        if available_sections:
            logger.info("Openings:")
            for section in available_sections:
                logger.info(f"  {section}")
        else:
            logger.info("Class is full.")

        return {"course": course, "available_sections": available_sections}

    @app.post("/subscribe")
    async def subscribe(sub: Sub, db: Session = Depends(get_db)):
        logger.info(f"subscribing: {sub}")
        if not sub.push_token.startswith("ExponentPushToken"):
            logger.error(f"{sub} is not a valid token")
            raise HTTPException(400, "Not an Expo push token")

        row = Subscriber(course=Sub.course, term=sub.term, token=sub.push_token)

        try:
            db.add(row)
            db.commit()
        except IntegrityError:
            db.rollback()
            return {"created": False}

        return {"created": True}

    @app.post("/unsubscribe")
    async def unsubscribe(sub: Sub, db: Session = Depends(get_db)):
        logger.info(f"UNsubscribing: {sub}")

        subscriber = db.get(
            Subscriber,
            {"course": sub.course, "term": sub.term, "token": sub.push_token},
        )

        if subscriber:
            db.delete(subscriber)
            db.commit()
            return {"deleted": True}

        return {"deleted": False}

    @app.on_event("startup")
    async def _startup() -> None:
        init_db()

    return app


if __name__ == "__main__":
    # running locally
    app = build_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=init_logging())
else:
    # for cloud server
    app = build_app()
