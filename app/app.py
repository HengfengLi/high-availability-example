import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restless import APIManager

app = Flask(__name__)
app.config['DEBUG'] = True
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hengfeng/code-lib/docker/ha/test.db'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@db:3306/myapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    suburb_name = db.Column(db.String(255))
    property_type = db.Column(db.String(100))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    carparks = db.Column(db.Integer)
    land_size = db.Column(db.Integer)
    price = db.Column(db.Float)
    sold_time = db.Column(db.DateTime(timezone=True), default=None)
    link = db.Column(db.String(255))


api_manager = APIManager(app, flask_sqlalchemy_db=db)
# http://127.0.0.1:5000/api/property
api_manager.create_api(Property, methods=['GET', 'POST'])
