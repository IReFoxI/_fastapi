import uvicorn
from fastapi import FastAPI
# from pydantic import BaseModel
# import time
import asyncio


app = FastAPI()


@app.get("/")
def home():
    # time.sleep(10)
    return {"message": "Hello World"}


@app.get("/{pk}")
async def get_item(pk: int, q: str = None):
    return {"key": pk, "q": q}

@app.get('/user/{pk}/items/{item}/')
async def get_user_item(pk: int, item: str):
    return {"user": pk, "item": item}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
