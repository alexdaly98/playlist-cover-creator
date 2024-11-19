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

Follow these steps to configure your Spotify credentials:

1. **Create Your Spotify Credentials:**
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Log in using your Spotify account.
   - Create a new app and select "Web API" as the API you plan to use.
   - In the "Redirect URIs" section, add: `http://127.0.0.1:8080/thumbnail-generator`.
   - After creating the app, you can see your app credentials in Basic Information.

2. **Allow User Login in the App:**
   - Navigate to `Settings > User Management` in the Spotify Developer Dashboard.
   - Add other users who require access so they can log in with their Spotify account.
   - Note: The account that created the App is allowed by default

3. **Update Redirect URI in the local code:**
   - Modify the redirect URI in `static/config.js` by updating it to:
     ```javascript
     export const redirectUri = 'http://127.0.0.1:8080/thumbnail-generator';
     ```
     
#### Google Credentials
GOOGLE_APPLICATION_CREDENTIALS is not mandatory (cf. Logging and Storage)

### Step 4: Run the Flask App locally:

- Start the application:
  ```bash
  python3 app.py
  ```

- Access the app at [http://localhost:8080](http://localhost:8080).


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
