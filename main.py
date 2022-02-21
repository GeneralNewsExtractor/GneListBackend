import pymongo
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel
from config_reader import conf
from fastapi.middleware.cors import CORSMiddleware


class Rule(BaseModel):
    data: Dict[str, str]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = pymongo.MongoClient(conf['mongo'])[conf['db']][conf['col']]


@app.get('/')
def index():
    return {'success': True}


@app.post('/rule')
def add_rule(rule: Rule):
    user_rule = rule.data
    handler.insert_one(user_rule)
    return {'success': True}


@app.get('/rule')
def get_rules():
    rules = handler.find({}, {'_id': 0})
    return {'success': True, 'rules': list(rules)}
