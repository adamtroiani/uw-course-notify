from fastapi import FastAPI, HTTPException, Depends
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from exponent_server_sdk import PushClient, PushMessage, PushServerError
import uvicorn, argparse, os
from check_availability import check_availability
from term import get_term_code
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import init_db
from models import Subscriber
from deps import get_db

import logging
from logging_config import init_logging
init_logging()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    course_code: str
    term_code:   int = get_term_code(next_term=True)

settings: Settings
push_client = PushClient()

class Sub(BaseModel):
    course: str
    push_token: str
    term: int

async def notify(course:str, open_sections:list[str], db: Session = Depends(get_db)):
    title = f"A seat opened in {course}!"
    body = ", ".join(open_sections)
        
    subscribed = select(Subscriber.token).where(Subscriber.course == course).distinct()
    for subscriber in db.scalars(subscribed):
        logger.info(f"notifying {subscriber} for {course}")
        message = PushMessage(
            to=subscriber,
            sound="default",
            title=title, body=body,
            data={"course": course, "available_sections": open_sections}
        )
        
        try:
            push_client.publish(message)
        except PushServerError as exc:
            logger.error(f"Failed for {subscriber}: {exc}")
    
def build_app(config: Settings) -> FastAPI:
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
    
    @app.get("/availability/{course}")
    async def availability(course:str):
        available_sections = check_availability(course, settings.term_code)
        
        if available_sections:
            logger.info("Openings:")
            for section in available_sections:
                logger.info(f"  {section}")
            await notify(config.course_code, open_sections)
        else:
            logger.info("Class is full.")
            
        return {"course": course, "available_sections": available_sections}

    @app.post("/subscribe")
    async def subscribe(sub: Sub, db: Session = Depends(get_db)):
        logger.info(f"subscribing: {sub}")
        if not sub.push_token.startswith("ExponentPushToken"):
            logger.error(f"{sub} is not a valid token")
            raise HTTPException(400, "Not an Expo push token")
        
        row = Subscriber(
            course = Sub.course,
            term = sub.term,
            token = sub.push_token
        )
        
        try:
            db.add(row)
            db.commit()
        except IntegrityError:
            db.rollback()
            return {"created": False}
            
        return {"created": True}    

    @app.on_event("startup")
    async def _startup() -> None:
        init_db()

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("course_code", help="e.g. 'CLAS 202'")
    args = parser.parse_args()

    settings = Settings(course_code=args.course_code)
    app       = build_app(settings)

    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    settings = Settings(course_code=os.getenv("COURSE_CODE", "CLAS 202"))
    app      = build_app(settings)
