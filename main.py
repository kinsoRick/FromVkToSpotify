import vk_api
from vk_api import audio
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import sys
import os
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
import re
from getpass import getpass
init()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

load_dotenv(resource_path(".env"))

def remove_text_between_parens(text):
    n = 1  # run at least once
    while n:
        text, n = re.subn(r'\([^()]*\)', '', text)
    return text 

login = input('Введите номер вк: ')
password = getpass('Введите пароль вк: ')
v_id = input('Введите id вк: ')
vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth()
vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

print("Ищем музыку...") 

a = vk_audio.get(owner_id=v_id) # Searching music in account

songs = []
uris = []
for element in a:
    print(f"{element['artist']} - {element['title']}")
    song = remove_text_between_parens(f"{element['artist']} - {element['title']}")
    songs.append(song)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))

user_id = sp.me()['id']
playlist = sp.user_playlist_create(user_id, "Песни из вк")['id']

for element in songs:
    try:
        result = sp.search(element)
        uris.append(result['tracks']['items'][0]['uri']) # Get uri from song 
        print(Fore.GREEN + element)
    except:
        print(Fore.RED + element)

i = 0
while i < len(uris):
    sp.playlist_add_items(playlist, uris[i:i+100]) # add song to playlist through uri songs
    i += 100

print("Проверьте плейлист! 🙃")
