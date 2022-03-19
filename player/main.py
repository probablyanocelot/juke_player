import requests
from dataclasses import dataclass
from producer import publish

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://test:test@db/player'
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    url = db.Column(db.String(200))


@dataclass
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user_in = db.Column(db.String(200))

    def serialize(self):
        return {"user_in": self.user_in}


@app.route('/api/songs')
def index():
    return jsonify(Song.query.all())


@app.route('/api/query/<string:user_in>')
def send_query(user_in):
    query = Query(user_in=user_in)
    # db.session.add(query)
    # db.session.commit()
    publish('query', query.serialize())
    return jsonify(query)


def user_input():
    user_in = input('Enter your query: ')
    # send_query(counter, user_in)
    req = requests.get('http://localhost:5000/api/query/{}'.format(user_in))
    user_input()


@app.route('/api/songs/<int:id>/like')
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)

    except:
        abort(400, "You already liked this product")

    return jsonify({
        'message': 'success',
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
