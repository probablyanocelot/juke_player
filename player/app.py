import requests
from dataclasses import dataclass
from producer import publish

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@db:5432/player'
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    url = db.Column(db.String(200))

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'url': self.url}


@dataclass
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user_in = db.Column(db.String(200))

    def serialize(self):
        return {'id': self.id, "user_in": self.user_in}


@app.route('/api/songs')
def index():
    return jsonify(Song.query.all())


@app.route('/api/songs/<int:id>/stream')
def get_stream_url(id):
    song = Song.query.get(id)
    song.url = url_to_stream(song.url)
    # publish('song_updated', song.serialize())
    return jsonify(song)


@ app.route('/api/query/<string:user_in>')
def send_query(user_in):
    query = Query(user_in=user_in)
    publish('query', query.serialize())
    return jsonify(query)


def user_input():
    user_in = input('Enter your query: ')
    # send_query(counter, user_in)
    req = requests.get('http://localhost:5000/api/query/{}'.format(user_in))
    user_input()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
