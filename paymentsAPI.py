from fastapi import FastAPI
from src import payments_v1, payments_v2, crud, models, schemas
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

def create_app():
    #f = open("payments.db", "x")

    app = FastAPI()

    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(payments_v1.router, prefix="/v1")
    app.include_router(payments_v2.router, prefix="/v2")

    return app

app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
