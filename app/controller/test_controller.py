from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/test")
def test():
    return "Hello World!"
