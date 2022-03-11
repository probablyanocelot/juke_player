from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://test:test@db/main'
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Song(db.Model):
    id: int
    title: str
    url: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    url = db.Column(db.String(1000))


@app.route('/api/songs')
def index():
    return jsonify(Song.query.all())


# @app.route('/api/songs/<int:id>')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
