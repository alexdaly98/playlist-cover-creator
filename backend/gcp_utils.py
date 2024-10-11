"""
This script handles logging image data and body parameters to a Google Cloud Storage bucket.
It provides functionality to download an image from a URL, save the image and body data locally, 
and upload them to a specified bucket. It is primarily designed for logging events related 
to a playlist cover creator.

Key Features:
- Downloads images from URLs.
- Saves JSON body data.
- Uploads images and JSON files to Google Cloud Storage, organized by a timestamp and user ID.

Environment:
- Google Cloud credentials should be set up to allow access to the Storage bucket.
"""

from google.cloud import storage
import os, json
from datetime import datetime
import pytz
import requests

# Bucket name where logs will be stored
bucket_name = "logs-playlist-cover-creator"

# Temporary local file paths for storing JSON and PNG files
local_temporary_json = 'local_temporary.json'
local_temporary_png = 'local_temporary.png'


def upload_file_to_bucket(local_filepath, destination_filepath, bucket_name=bucket_name):
    """
    Uploads a file to a specified Google Cloud Storage bucket.

    Args:
        local_filepath (str): Path to the local file to be uploaded.
        destination_filepath (str): Path inside the bucket where the file will be stored.
        bucket_name (str): The name of the bucket to upload the file to.
        
    Returns:
        None
    """
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_filepath)
    blob.upload_from_filename(local_filepath)
    return None


def log_image(image_url, body_data, log_type):
    """
    Logs an image and associated body data to the Google Cloud Storage bucket.

    Args:
        image_url (str): URL of the image to be downloaded and logged.
        body_data (dict): Dictionary containing the body data (e.g., request payload) to be logged.
        log_type (str): The type of log (e.g., 'success', 'error') that will dictate folder structure.
        
    Returns:
        None
    """
    france_tz = pytz.timezone('Europe/Paris')
    timestamp = datetime.now(france_tz).strftime('%Y%m%d_%H%M%S.%f')
    user_id_searched = body_data.get('user_id_searched', '')
    
    # Folder name based on timestamp and user ID
    folder_name = f"{timestamp}_user_{user_id_searched}"

    # Save body data as JSON and upload to bucket
    destination_filepath_json = os.path.join(log_type, folder_name, 'body_data.json')
    with open(local_temporary_json, 'w') as json_file:
        json.dump(body_data, json_file, indent=4)
    upload_file_to_bucket(local_temporary_json, destination_filepath_json, bucket_name=bucket_name)

    # Download the image and upload to bucket
    image_data = download_image(image_url)
    with open(local_temporary_png, 'wb') as f:
        f.write(image_data)
    destination_filepath_png = os.path.join(log_type, folder_name, 'image.png')
    upload_file_to_bucket(local_temporary_png, destination_filepath_png, bucket_name=bucket_name)
    return


def download_image(url):
    """
    Downloads an image from the provided URL.

    Args:
        url (str): URL of the image to be downloaded.
        
    Returns:
        bytes: Binary content of the image if the request is successful.
        
    Raises:
        Exception: If the image download fails (non-200 status code).
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")
