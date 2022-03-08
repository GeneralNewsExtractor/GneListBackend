import pymongo
from typing import Dict
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from config_reader import conf
from fastapi.middleware.cors import CORSMiddleware


class Rule(BaseModel):
    data: Dict[str, str]


class UpdateRule(BaseModel):
    rule_id: str
    url: str
    xpath: str
    name: str


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
    dedup = user_rule.pop('dedup')
    if not dedup:
        handler.insert_one(user_rule)
    else:
        handler.update_many({'name': user_rule['name']}, {'$set': user_rule}, upsert=True)
    return {'success': True}


@app.get('/rule')
def get_rules():
    rules = handler.find({})
    datas = []
    for rule in rules:
        rule['_id'] = str(rule['_id'])
        datas.append(rule)
    return {'success': True, 'rules': datas}


@app.delete('/rule/{rule_id}')
def delete_rules(rule_id: str):
    try:
        _id = ObjectId(rule_id)
    except Exception:
        return {'success': False, 'msg': 'rule id error!'}
    handler.delete_one({'_id': _id})
    return {'success': True}


@app.put('/rule')
def update_rule(rule: UpdateRule):
    try:
        _id = ObjectId(rule.rule_id)
    except Exception:
        return {'success': False, 'msg': 'rule id error!'}
    handler.update_one({'_id': _id},
                       {'$set': {'url': rule.url,
                                 'xpath': rule.xpath,
                                 'name': rule.name}})
    return {'success': True}
