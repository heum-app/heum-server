from fastapi import FastAPI
from app.api.routers import api_router

app = FastAPI(
    title="Heum",
    description="(Heum)",
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "HouseMate API 동작 중!"}
