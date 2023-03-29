from fastapi import FastAPI
from src import payments_v1, payments_v2, crud, models, schemas
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI()

    app.include_router(payments_v1.router, prefix="/v1")
    app.include_router(payments_v2.router, prefix="/v2")

    return app

app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
