import os
import requests
import getreddit
import json
from dataclasses import dataclass
from producer import publish

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@db:5432/dj'
app.config['SQLALCHEMY_ECHO'] = True

CORS(app)

db = SQLAlchemy(app)

db.drop_all()
db.create_all()
migrate = Migrate(app, db)


@dataclass
class Song(db.Model):
    __tablename__ = 'songs'
    # __table_args__ = {''}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000))
    url = db.Column(db.String(200))

    # UniqueConstraint('id', 'url', name='id_url_unique')

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'url': self.url}


# @dataclass
# class Playlist(Song):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=False)


@dataclass
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user_in = db.Column(db.String(200))

    def serialize(self):
        # 'user_in': self.user_in
        return {'id': self.id, 'user_in': self.user_in}


@app.route('/api/songs')
def index():
    return jsonify(Song.query.all())


@app.route('/api/<string:cmd>/<string:terms>')
def make_playlist(cmd, terms):
    if cmd == 'r':
        # print(f"user in {terms}")
        dirty_terms = json.loads(getreddit.get_yt_subs(terms))
        # publish('song', song.serialize(), service='dj')
        # requests.get(
        #     'http://localhost:5000/api/songs/{}/add'.format(song.id))
        return jsonify(dirty_terms)


@app.route('/api/songs/<int:id>/add')
def add_song(id, song):
    db.session.add(song)
    db.session.commit()
    publish('song', song.serialize())
    print('Song Added!')

# @app.route('/api/query/<string:user_in>')
# def query(user_in):
#     query = Query(user_in=user_in)
#     db.session.add(query)
#     db.session.commit()
#     publish('query', query)
#     return jsonify(query)


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
    app.run(debug=True, host='0.0.0.0', port=5000)
