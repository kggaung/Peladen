from fastapi import FastAPI

from app.controller import test_controller

app = FastAPI()

app.include_router(test_controller)
