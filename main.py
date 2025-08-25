from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import BaseModel
from exponent_server_sdk import PushClient, PushMessage, PushServerError
import uvicorn
from check_availability import check_availability, req_course_data
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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        body = (await request.body()).decode("utf-8", "ignore")[:2000]
        logger.error("422 on %s %s\nerrors=%s\nbody=%s",
                    request.method, request.url.path, exc.errors(), body)
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
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
        logger.info(f"Subscribing: {sub.push_token} to {sub.course}...")
        if not sub.push_token.startswith("ExponentPushToken"):
            logger.error(f"{sub} is not a valid token")
            raise HTTPException(400, "Not an Expo push token")

        resp, course_exists = req_course_data(sub.course, sub.term)
        if not course_exists:
            logger.error(
                f"Subscribe failed: {sub.course} ({sub.term}) is not a valid course"
            )
            raise HTTPException(404, "Subscription failure: course does not exist")

        row = Subscriber(course=sub.course, term=sub.term, token=sub.push_token)

        try:
            db.add(row)
            db.commit()
        except IntegrityError:
            db.rollback()
            logger.exception("Insert failed")
            return {"created": False}

        logger.info("Successfully subscribed")
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
