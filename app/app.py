from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Response, request, make_response, jsonify
import json
import arrow
import redis

app = Flask(__name__)
app.config['DEBUG'] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@db:3306/myapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
rds = redis.StrictRedis('redis_master', 6379)


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

    def json(self):
        return {
            'id': self.id,
            'address': self.address,
            'suburb_name': self.suburb_name,
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'carparks': self.carparks,
            'land_size': self.land_size,
            'price': self.price,
            'sold_time': str(arrow.get(self.sold_time)),
            'link': self.link
        }


@app.route('/api/property', methods=['GET', 'POST'])
def api_property():
    if request.method == 'GET':
        start = request.args.get('start', '')
        start = int(start) if start.isdigit() else 0

        data = rds.get(f'property_start_from_{start}')

        if data:
            return data

        properties = Property.query.order_by(Property.sold_time).limit(10).offset(start).all()
        properties_list = [prop.json() for prop in properties]
        data = json.dumps(properties_list)
        rds.set(f'property_start_from_{start}', data, 3600)
        return jsonify(properties_list)
    else:
        kwargs = request.get_json(force=True)
        new_property = Property(**kwargs)
        db.session.add(new_property)
        db.session.commit()
