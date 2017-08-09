from flask import Flask, render_template
from peewee import *

import datetime
import sqlite3

db = SqliteDatabase('ServiceDesk.db')

# BaseModel
class BaseModel(Model):
    class Meta:
        database = db


# User Model
#class User(BaseModel):
#    name = CharField()
    
    
# Incident model
class Incident(BaseModel):
    created_date = DateTimeField(default=datetime.datetime.now)
    incident = CharField()
    url = CharField()
    description = TextField()
    is_closed = BooleanField(default=False)
        
    class Meta:
        order_by = ('-created_date', )
        
        
        
# init the connection to DB
def initialize():
    db.connect()
    db.create_tables([Incident], safe=True)
    db.close()