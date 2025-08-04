from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
import uvicorn, argparse, os

from check_availability import check_availability
# from push import notify_ios_clients
from term import get_term_code

class Settings(BaseSettings):
    course_code: str
    term_code:   int = get_term_code(next_term=True)

settings: Settings

def build_app(config: Settings) -> FastAPI:
    app = FastAPI(
        title="UW Notify API",
        version="0.0.0",
    )

    @app.get("/availability/{course}")
    async def availability(course:str):
        available_sections = check_availability(course, settings.term_code)
        return {"course": course, "available_sections": available_sections}
        
    @repeat_every(seconds=5)
    async def poll_open_seats() -> None:
        open_sections = check_availability(
            config.course_code,
            config.term_code
        )
        if open_sections:
            print(open_sections)
            # await notify_ios_clients(open_sections)
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
