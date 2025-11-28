from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.food_detection import router as food_router

import os

app = FastAPI()


"""
from app.routes.food import router as food_router
from app.routes.user import router as user_router

app = FastAPI()

app.include_router(food_router)
app.include_router(user_router)
"""



app.include_router(food_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("APP_BASE_URL")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

