from backend import spotify_api, openai_utils
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
    if creation_method == 'track_thumbnails':
        # Extract image URLs from the data
        image_urls = [track['image_url'] for track in tracks]
        url_output = openai_utils.fusion_images(image_urls, mood)
    elif creation_method == 'titles_artists':
        url_output = openai_utils.fusion_titles_artists(tracks, mood)
    else:
        jsonify({'error': 'Creation method not permitted'}), 400

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
        return jsonify({'message': 'Image uploaded successfully!'}), 200
    else:
        return jsonify({'error': 'Failed to upload image'}), upload_response.status_code



# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the thumbnail generator
@app.route('/thumbnail-generator')
def thumbnail_generator():
    return render_template('thumbnailGenerator.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
