from fastapi import FastAPI
from src import payments_v1, payments_v2


def create_app():
    app = FastAPI()

    app.include_router(payments_v1.router, prefix="/payments")
    app.include_router(payments_v2.router, prefix="/payments")

    return app

app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}

