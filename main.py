from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="FastAPI App"
)


fake_users = [
    {'id': 1, 'name': 'Nikita', 'role': 'admin', 'bank': 100.2},
    {'id': 2, 'name': 'Anton', 'role': 'trader', 'bank': 500.0},
]

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    name: str
    role: str
    bank: float
    degree: Optional[List[Degree]] = "no degre :("


@app.get('/users/{user_id: int}', response_model=List[User])
async def get_users(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


fake_trades = [
    {'id': 1, 'user_id': 1,'currency': 'BTC', 'price': 232.2},
    {'id': 2, 'user_id': 2, 'currency': 'RUB', 'price': 10001.12},
]


@app.get('/trades')
async def get_trades(offset:int = 0, limit:int = 10):
    return fake_trades[offset:limit]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=10)
    price: float = Field(ge=0)


@app.post('/add_trades')
async def add_trades(trades: List[Trade]):
    fake_trades.append(trades)
    return {'status': 200, 'fake_trades': fake_trades}
    