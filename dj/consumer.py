import pika
# from dotenv import load_dotenv
import os
import json
import requests
import pafy
from search_yt import yt_query, YT_API_KEY, get_vid_name
from app import Song, Query, db
from dotenv import load_dotenv
load_dotenv('.env')

MQ_HOST = os.getenv('MQ_HOST')

params = pika.URLParameters(MQ_HOST)

# params = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=pika.credentials.PlainCredentials(
#     MQ_USER, MQ_PASSWD), heartbeat_interval=0)
# conn = pika.BlockingConnection(parameters=params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='dj')


def callback(ch, method, properties, body):
    print('Received in DJ')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'query':  # properties.content_type == 'query':
        query = Query(id=data['id'], user_in=data['user_in'])
        print(query.user_in)
        cmd = query.user_in.split(' ')[0]
        terms = ' '.join(query.user_in.split(' ')[1:])

        if cmd == 'r':
            print('Reddit')
            playlist = requests.get(
                'http://backend:5000/api/{}/{}'.format(cmd, terms), verify=False).json()
            for entry in playlist:
                print(entry)
                track = req[item]
                print(track)
                # song_with_name = get_vid_name(YT_API_KEY, track)
                # song = Song(title=song_with_name['title'], url=track['url'])
                # print(song.title)
                # song.title = get_vid_name(YT_API_KEY, song.url)

                # # print(vars(song))
                # db.session.add(song)
                # db.session.commit()
                # print("Song Created")
            # print(' '.join(query.user_in.split(' ')[1:]))  # USE FOR YOUTUBE!!!

    elif properties.content_type == 'song':
        song = Song(title=data['title'], url=data['url'])
        db.session.add(song)
        db.session.commit()
        print("Song Created")

    # elif properties.content_type == 'yt_playlist':
        # playlist = Playlist(id=data['id'], user_in=data['user_in'])
        # db.session.add(song)
        # db.session.commit()
        # print('Song Created')

    elif properties.content_type == 'song_updated':
        song = Song.query.get(data['id'])
        song.title = data['title']
        song.image = data['url']
        db.session.commit()
        print('Song Updated')

    elif properties.content_type == 'song_deleted':
        song = Song.query.get(data)
        db.session.delete(song)
        db.session.commit()
        print('Song Deleted')


channel.basic_consume(queue='dj',
                      on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
