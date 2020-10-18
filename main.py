import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
# import time
from requests_html import HTMLSession


app = FastAPI()
session = HTMLSession()


db = []


class City(BaseModel):
    name: str
    timezone: str


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        with session.get(f"http://worldtimeapi.org/api/timezone/{city['timezone']}") as response:
            results.append({'name': city['name'],
                            'timezone': city['timezone'],
                            'current_time': response.json()['datetime']
                            })
    return results

@app.get('/cities/{city_id}')
def get_citi(city_id: int):
    city = db[city_id]
    with session.get(f"http://worldtimeapi.org/api/timezone/{city['timezone']}") as response:
        return {'name': city['name'],
                'timezone': city['timezone'],
                'current_time': response.json()['datetime']}

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id)
    return 'Deleted'


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
