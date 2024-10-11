# Spotify Playlist Cover Creator

Welcome to the Spotify Playlist Cover Creator! This project allows you to AI-generate custom covers for your Spotify public playlists by blending track images or details (titles and artists), and then uploading them back to Spotify. It uses a Flask-based backend that integrates seamlessly with the Spotify API, OpenAI, and Google Cloud Platform (GCP) for comprehensive logging and image storage.

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
git clone https://github.com/alexdaly98/playlist-cover-creator.git
cd playlist-cover-creator
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
  GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
  ```

#### Setting Up Spotify Credentials

You can create your own Spotify credentials here [https://developer.spotify.com/](https://developer.spotify.com/).<br>
Log into the dashboard using your Spotify account.<br>
Create an app and select "Web API" for the question asking which APIs you are planning to use.<br>
Add `http://127.0.0.1:8080/thumbnail-generator` to the "redirect URIs" section.<br>
Once you have created your app, you will have access to the app credentials.<br><br>

To allow other users to log in to their spotify account within the project app you must add them in Settings>User Management.

#### Google Credentials
GOOGLE_APPLICATION_CREDENTIALS is not mandatory (cf. Logging and Storage)

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

### GCP Bucket Setup

If you choose **not** to set up logging, the app will still function normally without storing event data.<br>

To use this feature, you must set up a GCP bucket and provide your credentials as an environment variable. Follow these steps:

1. **Generate a Service Account Key:**
   - Create a key associated with your GCP service account.

2. **Update .env File:**
   - Add the following line to your `.env` file:
     ```plaintext
     GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
     ```
   - Replace `path/to/your/service-account-key.json` with the actual path to your downloaded service account key.
