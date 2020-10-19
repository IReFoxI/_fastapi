import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from requests_html import HTMLSession

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


app = FastAPI()
session = HTMLSession()


db = []


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)

City_Pydantic = pydantic_model_creator(City, name='City')
CityIn_Pydantic = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)


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

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models':['main']},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
