import uvicorn

from fastapi import FastAPI, APIRouter
from api.routers import message, user, thread


app = FastAPI()

api_router = APIRouter(
    prefix='/api',
    tags=['API']
)


api_router.include_router(message.router)
api_router.include_router(user.router)
api_router.include_router(thread.router)


app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
