"""
This script interacts with the Spotify Web API to retrieve playlists, fetch tracks, and upload playlist
thumbnails. It also compresses and encodes images to meet Spotify's payload size constraints for playlist covers.

Key Features:
- Retrieves user playlists and tracks.
- Compresses and Base64 encodes images.
- Uploads playlist thumbnails to Spotify.

Environment Variables Used:
- Spotify API credentials should be set in a separate `config.py` file, with 
  SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64
from io import BytesIO
from PIL import Image
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


# Set up Spotify authentication
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_playlists(user_id):
    """
    Fetches all playlists for a given Spotify user.

    Args:
        user_id (str): The Spotify user ID to fetch playlists for.

    Returns:
        list: A list of simplified playlists, each containing:
            - 'id' (str): Playlist ID.
            - 'image_url' (str): URL of the playlist image.
            - 'name' (str): Playlist name.
            - 'track_count' (int): Number of tracks in the playlist.
    """
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
        'image_url': p['images'][0]['url'] if p['images'] else '',
        'name': p['name'],
        'track_count': p['tracks']['total']
    } for p in playlists]

    return simplified_playlists


def get_playlist_tracks(playlist_id):
    """
    Fetches all tracks from a given Spotify playlist.

    Args:
        playlist_id (str): The Spotify playlist ID to fetch tracks from.

    Returns:
        list: A list of simplified tracks, each containing:
            - 'id' (str): Track ID.
            - 'name' (str): Track name.
            - 'artist' (str): Artists performing the track (comma-separated if multiple).
            - 'image_url' (str): URL of the track's album image.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Handle pagination if playlist has more than 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Simplify the data structure for the frontend
    simplified_tracks = []
    for t in tracks:
        try:
            simplified_track = {
            'id': t['track']['id'],
            'name': t['track']['name'],
            'artist': ', '.join([artist['name'] for artist in t['track']['artists']]),
            'image_url': t['track']['album']['images'][0]['url'] if t['track']['album']['images'] else ''
            }
            simplified_tracks.append(simplified_track)
        except:
            Warning('A track was skipped')
    return simplified_tracks


def get_base64_encoded_image(url: str, max_size_kb: int = 32) -> str:
    """
    Downloads an image from a URL, compresses it, and returns a Base64-encoded JPEG.

    Args:
        url (str): URL of the image to download.
        max_size_kb (int, optional): Maximum allowed size for the encoded image (in KB). Defaults to 32 KB.

    Returns:
        str: The Base64-encoded string representation of the image.
    """
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
    """
    Uploads a playlist thumbnail image to Spotify after compressing it.

    Args:
        playlist_id (str): The Spotify playlist ID.
        image_url (str): URL of the image to upload as the thumbnail.
        access_token (str): OAuth access token for Spotify API.
        max_size_kb (int): Maximum allowed size for the image (in KB).

    Returns:
        requests.Response: The response object from the Spotify API.
    """
    base64_image_string = get_base64_encoded_image(image_url, max_size_kb=max_size_kb)
    
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


def upload_playlist_thumbnail_multiple_try(playlist_id, image_url, access_token):
    """
    Attempts to upload a playlist thumbnail multiple times with progressively smaller image sizes.
    Theses different max_size_kb attemps have been chosen after personally trying different image sizes to upload, Spotify API 
        rejecting threshold being unpredictable when experimenting...

    Args:
        playlist_id (str): The Spotify playlist ID.
        image_url (str): URL of the image to upload as the thumbnail.
        access_token (str): OAuth access token for Spotify API.

    Returns:
        requests.Response: The response object from the final attempt.
    """
    upload_response = upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=55)
    if not upload_response.ok:
        upload_response = upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=50)
    if not upload_response.ok:
        upload_response = upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=45)
    
    return upload_response
