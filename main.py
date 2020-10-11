import uvicorn
from fastapi import FastAPI
# from pydantic import BaseModel
# import time
import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    # time.sleep(10)
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    list = []
    list2 = []

    async def first():
        for i in range(2):

            list.append(i)
        await asyncio.sleep(3)
        print(list)

    async def second():
        for i in range(10):
            list2.append(i)
        print(list2)

    await first()
    await second()
    
    return {"user_id": user_id, 'list': list, 'list2':list2}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
