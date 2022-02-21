import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Type the date you want to go too, yyyy-mm-dd : ")
DATE = "2000-08-12"
response = requests.get(f"https://www.billboard.com/charts/hot-100/{DATE}/")

top100_page = response.text
soup = BeautifulSoup(top100_page, "html.parser")
songs_tags = soup.find_all("h3", class_="c-title")
songs_data = [song.getText() for song in songs_tags]
songs = songs_data[7:404:4]
# print(*songs, sep="\n")


Client_ID = "a20c7216abc948fcb1614032dd4ddaeb"
Client_secret = "###############"
URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

songs_uris = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
       pass

new_playlist = sp.user_playlist_create(name=f"billboard 100 - {date}", user=user_id, public=False)
sp.playlist_add_items(playlist_id=new_playlist["id"], items=songs_uris)


