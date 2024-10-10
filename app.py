from backend import spotify_api, openai_utils, gcp_utils
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', template_folder='templates')
CORS(app)


@app.route('/playlists/<user_id>', methods=['GET'])
def get_playlists(user_id):
    simplified_playlists = spotify_api.get_playlists(user_id)
    return jsonify(simplified_playlists)


@app.route('/tracks/<playlist_id>', methods=['GET'])
def get_playlist_tracks(playlist_id):
    simplified_tracks = spotify_api.get_playlist_tracks(playlist_id)
    return jsonify(simplified_tracks)


@app.route('/thumbnail/<creation_method>', methods=['POST'])
def generate_thumbnail(creation_method):
    # Parse JSON request body
    data = request.get_json()
    tracks = data.get('tracks', [])
    mood = data.get('mood', '')
    playlist_data = data.get('selected_playlist', {})
    include_title = data.get('include_title', False)

    playlist_title = ''
    if include_title:
        playlist_title = playlist_data['name']

    if creation_method == 'track_thumbnails':
        # Extract image URLs from the data
        image_urls = [track['image_url'] for track in tracks]
        url_output = openai_utils.fusion_images(image_urls, mood, playlist_title)
    elif creation_method == 'titles_artists':
        url_output = openai_utils.fusion_titles_artists(tracks, mood, playlist_title)
    else:
        jsonify({'error': 'Creation method not permitted'}), 400
    
    gcp_utils.log_image_creation(url_output, data)

    return jsonify({"image_url": url_output})


@app.route('/upload-playlist-image', methods=['POST'])
def upload_playlist_image():
    data = request.get_json()
    playlist_id = data.get('playlist_id')
    image_url = data.get('image_url')
    access_token = data.get('access_token')

    if not playlist_id or not image_url or not access_token:
        return jsonify({'error': 'Missing parameters'}), 400

    upload_response = spotify_api.upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=55)
    if not upload_response.ok:
        upload_response = spotify_api.upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=50)
    if not upload_response.ok:
        upload_response = spotify_api.upload_playlist_thumbnail(playlist_id, image_url, access_token, max_size_kb=45)
    if upload_response.ok:
        gcp_utils.log_image_upload(image_url, data)
        return jsonify({'message': 'Image uploaded successfully!'}), 200
    else:
        return jsonify({'error': 'Failed to upload image'}), upload_response.status_code



# Route for the main page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/playlist-explorer')
def playlist_explorer():
    return render_template('playlistExplorer.html')

# Route for the thumbnail generatorc
@app.route('/thumbnail-generator')
def thumbnail_generator():
    return render_template('thumbnailGenerator.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
