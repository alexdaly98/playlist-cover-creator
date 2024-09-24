import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64
from io import BytesIO
from PIL import Image
import requests
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_playlists(user_id):
    playlists = []
    limit = 50
    offset = 0

    while True:
        response = sp.user_playlists(user_id, limit=limit, offset=offset)
        playlists.extend(response['items'])
        if len(response['items']) < limit:
            break
        offset += limit

    # Simplify the data structure for the frontend
    simplified_playlists = [{
        'id': p['id'],  # Include the playlist ID for fetching tracks
        'playlist_image': p['images'][0]['url'] if p['images'] else '',
        'playlist_name': p['name'],
        'track_count': p['tracks']['total']
    } for p in playlists]

    return simplified_playlists


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Handle pagination if playlist has more than 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Simplify the data structure for the frontend
    simplified_tracks = [{
        'track_name': t['track']['name'],
        'artist': ', '.join([artist['name'] for artist in t['track']['artists']]),
        'image_url': t['track']['album']['images'][0]['url'] if t['track']['album']['images'] else ''
    } for t in tracks]

    return simplified_tracks



def get_base64_encoded_image(url: str, max_size_kb: int = 32) -> str:
    # Download the image from the URL
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    
    # Define a buffer to save the image
    buffer = BytesIO()
    
    # Compress the image and ensure it's under the maximum size
    quality = 95
    while True:
        buffer.seek(0)
        buffer.truncate()
        image.save(buffer, format='JPEG', quality=quality)
        buffer_size_kb = len(buffer.getvalue()) / 1024
        
        if buffer_size_kb <= max_size_kb:
            break
        
        quality -= 1
    
    # Encode the image data to Base64
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return encoded_image


def upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb):

    base64_image_string = get_base64_encoded_image(image_url, max_size_kb = max_size_kb)
    # Upload the image to Spotify
    upload_response = requests.put(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/images',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'image/jpeg'
        },
        data=base64_image_string
    )

    return upload_response
