import vlc
import requests
from app import user_input
from models import Song


class Player(Object):
    def __init__(self, json_data):
        self.Instance = vlc.Instance()  # "prefer-insecure"
        self.media_player = vlc.MediaListPlayer()
        self.playlist = self.Instance.media_list_new()
        self.counter = 0
        self.queue_song()

    def queue_song(self):
        # song = Song.query.get(self.counter)
        res = requests.get(
            'http://backend:5000/api/songs/{}/stream'.format(self.counter)).json()
        song = Song(res['id'], res['title'], res['url'])
        Media = self.Instance.media_new(song.url)
        Media.get_mrl()
        self.playlist.add_media(Media)
        self.media_player.set_media_list(self.playlist)

    def next_song():
        self.counter += 1
        queue_song()
        self.media_player.next()

    keyboard.add_hotkey(r'ctrl + alt + 8',
                        lambda: self.media_player.previous())
    keyboard.add_hotkey(r'ctrl + alt + 9', lambda: self.media_player.pause())
    keyboard.add_hotkey(r'ctrl + alt + 0', lambda: next_song())

    media_player.play()
    print('after play')
    # media_player.play_item_at_index(0)
    print('after play_item_at_index')
    keyboard.wait(r'ctrl + alt + q')
    media_player.stop()
    user_input()
