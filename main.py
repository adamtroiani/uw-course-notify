from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from exponent_server_sdk import PushClient, PushMessage, PushServerError
import uvicorn, argparse, os
from check_availability import check_availability
from term import get_term_code
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware

class Settings(BaseSettings):
    course_code: str
    term_code:   int = get_term_code(next_term=True)

settings: Settings
push_client = PushClient()

subscriptions = defaultdict(list)
class Sub(BaseModel):
    course: str
    push_token: str

async def notify(course:str, open_sections:list[str]):
    print(f"notifying: {subscriptions[course]}")
    
    title = f"A seat opened in {course}!"
    body = ", ".join(open_sections)
        
    for token in subscriptions[course]:
        message = PushMessage(
            to=token,
            sound="default",
            title=title, body=body,
            data={"course": course, "available_sections": open_sections}
        )
        
        try:
            push_client.publish(message)
        except PushServerError as exc:
            print(f"Failed for {token}: {exc}")
    
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
        return {"course": course, "available_sections": available_sections}

    @app.post("/subscribe")
    async def subscribe(sub: Sub):
        print(f"subscribing: {sub}")
        if not sub.push_token.startswith("ExponentPushToken"):
            raise HTTPException(400, "Not an Expo push token")
        subscriptions[sub.course].append(sub.push_token)
        return {"ok": True}

    @repeat_every(seconds=5)
    async def poll_open_seats() -> None:
        open_sections = check_availability(
            config.course_code,
            config.term_code
        )
        
        if open_sections:
            print("Openings:")
            for section in open_sections:
                print(f"  {section}")
            await notify(config.course_code, open_sections)
        else:
            print("Class is full.")

    @app.on_event("startup")
    async def _startup() -> None:
        await poll_open_seats()

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
