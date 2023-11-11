from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}


post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


kind_types = {'terrier', 'bulldog', 'dalmatian'}


@app.get('/')
def root():
    return "UwU"


@app.post('/post')
def post():
    post_db.append(Timestamp(id=post_db[-1].id + 1, timestamp=int(time.time())))
    return post_db[-1]


@app.get('/dog')
def get_dogs(kind):
    if kind in kind_types:
        return [v for k, v in dogs_db.items() if v.kind==kind]
    elif kind is None:
        return [v for k, v in dogs_db.items()]
    raise HTTPException(status_code=422, detail='Ошибка в данных')


@app.post('/dog')
def post_dog(name, pk, kind):
    if pk not in dogs_db.keys() and kind in kind_types and name:
        dogs_db[pk] =  Dog(name=name, pk=pk, kind=DogType(kind))
        return dogs_db[pk]
    raise HTTPException(status_code=422, detail='Ошибка в данных')


@app.get('/dog/{pk}')
def get_dog_pk(pk):
    if pk in dogs_db.keys():
        return dogs_db[pk]
    raise HTTPException(status_code=422, detail='Ошибка в данных')
    

@app.patch('/dog/{pk}')
def upd_dog(name, pk, kind):
    if pk in dogs_db.keys() and kind in kind_types and name:
        dogs_db[pk] = Dog(name=name, pk=pk, kind=DogType(kind))
        return dogs_db[pk]
    raise HTTPException(status_code=422, detail='Ошибка в данных')
    