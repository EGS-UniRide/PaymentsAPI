from fastapi import FastAPI
from src import payments_v1, payments_v2, crud, models, schemas
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import dotenv_values

#models.Base.metadata.create_all(bind=engine)

config = dotenv_values(".env")

def create_app():

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

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["DB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}
