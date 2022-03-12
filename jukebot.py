import pafy
import vlc
import json
import pandas as pd
import keyboard
import getreddit
from tabulate import tabulate


# json data from reddi-bot -> pandas dataframe
def get_library(datafile):
    df = pd.read_json(datafile)
    return(df.T)


def get_url(library, counter=None):
    post = library.loc[counter]
    domain = post['domain']
    url = post['url']
    return url


# link handling youtube-dl (used in pafy)
# do get_bestquality().url to get the url of the best quality
def get_bestquality(url, watch=False):
    video = pafy.new(url)
    if watch:
        best = video.getbest()
    else:
        best = video.getbestaudio()
    return best


def is_yt(library, counter=None):
    try:
        url = url.replace(r'youtu.be', r'youtube.com/v/')
        url = url.replace(r'watch?v=', 'v/')
        test_url = get_bestquality(url)

        return url
    except ValueError:
        library = library.drop(labels=counter, axis=0)
        library = library.reset_index(drop=True)
        return library

# displays current song info in terminal


def song_info(library, counter=None):
    show_info = print(tabulate(
        (
            # metadata_key : metadata_value of current song
            [metadata, library[metadata][counter]]
            for metadata in library), headers=['Song No. ' + str(counter), 'Now Playing'], tablefmt='pretty'))
    return show_info


def song_to_playlist(Instance, playlist, url):
    # player = Instance.media_player_new()
    Media = Instance.media_new(url)
    Media.get_mrl()

    # adding media to media list
    playlist.add_media(Media)


def main(library, count):

    # player objects
    Instance = vlc.Instance()  # "prefer-insecure"
    media_player = vlc.MediaListPlayer()
    playlist = Instance.media_list_new()

    print(library['url'])
    song_info(library, counter=count)

    for url in library['url']:
        print(url)

        # try:

        url = url.replace(r'youtu.be/', 'youtube.com/watch?v=')

        if url.split('&amp;')[0]:
            url = url.split('&amp;')[0]

        yt_url = get_bestquality(url).url
        yt_title = get_bestquality(url).title
        # print(yt_url, yt_title)

        library.at[count, 'url'] = yt_url
        library.at[count, 'title'] = yt_title

        count += 1

        song_to_playlist(Instance, playlist, yt_url)
        # except:
        #     print('except!')
        #     library.drop(labels=count, axis=0)
        #     library.reset_index(drop=True)
    print(len(playlist))
    print(library)
    media_player.set_media_list(playlist)
    keyboard.add_hotkey(r'ctrl + alt + b', lambda: media_player.previous())
    keyboard.add_hotkey(r'ctrl + alt + n', lambda: media_player.next())
    keyboard.add_hotkey(r'ctrl + alt + space', lambda: media_player.pause())
    media_player.play()
    print('after play')
    # media_player.play_item_at_index(0)
    print('after play_item_at_index')
    keyboard.wait(r'ctrl + alt + q')


if __name__ == '__main__':
    edm_posts = getreddit.post_data('edm', 50)
    edm_yt = getreddit.filter_data(edm_posts, 'youtu')
    edm_library = get_library(edm_yt)
    main(edm_library, 0)
