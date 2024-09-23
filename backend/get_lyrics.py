import requests


def get_lyrics(artist, song):
    short_artist = artist.split(',')[0]
    response = requests.get(f'https://api.lyrics.ovh/v1/{short_artist}/{song}')

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response body (in JSON format)
        return response.json()['lyrics']
    else:
        return ''
    
artist = 'Robin Thicke'
song='Blurred Lines'