# Spotify Playlist Cover Creator

Welcome to the Spotify Playlist Cover Creator! This project helps you design custom thumbnails for your Spotify playlists by blending track images or details (titles and artists), and then uploading them back to Spotify. It uses a Flask-based backend that integrates seamlessly with the Spotify API, OpenAI, and Google Cloud Platform (GCP) for comprehensive logging and image storage.

## Features

- **Spotify Playlist Explorer:** Easily browse and view your playlists and their tracks on Spotify.
- **Thumbnail Generation:**
  - Create thumbnails using track images or track titles and artists.
  - Generate thumbnails based on custom moods and titles.
  - Utilize OpenAI models for creative image blending and description creation.
- **Playlist Thumbnail Upload:** Directly upload the custom thumbnails to your Spotify playlists.
- **GCP Integration:** Log and store all image generation and upload activities in GCP buckets for easy retrieval and analysis.

## Tech Stack

- **Backend:** Flask, Python
- **APIs:**
  - Spotify API for accessing playlist and track information.
  - OpenAI for image blending and description generation.
  - GCP for logging and storage functions.
- **Frontend:** HTML, CSS, JavaScript (using Flask template rendering)
- **Deployment:** Configured for deployment on Google Cloud, such as Cloud Run.

## Installation

### Step 1: Clone the Repository:
```bash
git clone https://github.com/your-repository-url.git
cd your-repository-folder
```

### Step 2: Set Up the Environment:

- **Create a Virtual Environment:**
  ```bash
  python3 -m venv cover_env
  source cover_env/bin/activate
  ```

- **Install the Required Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

### Step 3: Configure Environment Variables:

- Create a `.env` file and include the following API keys and credentials:
  ```makefile
  SPOTIFY_CLIENT_ID=your_spotify_client_id
  SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
  OPENAI_API_KEY=your_openai_api_key
  ```

### Step 4: Run the Flask App locally:

- Start the application:
  ```bash
  python app.py
  ```

- Access the app at [http://localhost:8080](http://localhost:8080).

## Endpoints

- **GET /playlists/**: Fetch the specified user's playlists.
- **GET /tracks/**: Retrieve tracks from a specific playlist.
- **POST /thumbnail/**: Generate a playlist thumbnail using track images or titles/artists.
- **POST /upload-playlist-image**: Uploads the generated thumbnail to a specified Spotify playlist.
- **GET /**: Main landing page (HTML).
- **GET /playlist-explorer**: Explore your playlists (HTML).
- **GET /thumbnail-generator**: Generate playlist thumbnails (HTML).

## Usage

- **Navigate to the Playlist Explorer:** Enter your Spotify user ID to browse your playlists and tracks.
- **Generate Thumbnails:** Select a playlist and choose a thumbnail generation method—either through track images or track titles/artists.
- **Upload to Spotify:** After generating a thumbnail, upload it directly to your Spotify playlist from the app interface.

## Logging and Storage

All events related to image generation and uploads are recorded in a GCP bucket. Each event is organized in a timestamped folder containing the generated image and relevant metadata for easy tracking and analysis.
