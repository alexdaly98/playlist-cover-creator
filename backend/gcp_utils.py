from google.cloud import storage
import os, json
from datetime import datetime
import pytz
import requests
#To load GOOGLE_APPLICATION_CREDENTIALS env variable
import config

bucket_name = "logs-playlist-cover-creator"

local_temporary_json = 'local_temporary.json'
local_temporary_png = 'local_temporary.png'


def upload_file_to_bucket(local_filepath, destination_filepath, bucket_name=bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_filepath)
    blob.upload_from_filename(local_filepath)
    return None


def log_image_creation(image_url, body_data):
    france_tz = pytz.timezone('Europe/Paris')
    timestamp = datetime.now(france_tz).strftime('%Y%m%d_%H%M%S.%f')
    user_id_searched = body_data.get('user_id_searched', '')
    folder_name = f"{timestamp}_user_{user_id_searched}"

    destination_filepath_json = os.path.join('creation', folder_name, 'body_data.json')
    with open(local_temporary_json, 'w') as json_file:
        json.dump(body_data, json_file, indent=4)
    upload_file_to_bucket(local_temporary_json, destination_filepath_json, bucket_name=bucket_name)

    image_data = download_image(image_url)
    with open(local_temporary_png, 'wb') as f:
        f.write(image_data)
    destination_filepath_png = os.path.join('creation', folder_name, 'image.png')
    upload_file_to_bucket(local_temporary_png, destination_filepath_png, bucket_name=bucket_name)
    return


def log_image_upload(image_url, body_data):
    france_tz = pytz.timezone('Europe/Paris')
    timestamp = datetime.now(france_tz).strftime('%Y%m%d_%H%M%S.%f')
    user_id_searched = body_data.get('user_id_searched', '')
    folder_name = f"{timestamp}_user_{user_id_searched}"

    destination_filepath_json = os.path.join('upload', folder_name, 'body_data.json')
    with open(local_temporary_json, 'w') as json_file:
        json.dump(body_data, json_file, indent=4)
    upload_file_to_bucket(local_temporary_json, destination_filepath_json, bucket_name=bucket_name)
    
    image_data = download_image(image_url)
    destination_filepath_png = os.path.join('upload', folder_name, 'image.png')
    with open(local_temporary_png, 'wb') as f:
        f.write(image_data)
    upload_file_to_bucket(local_temporary_png, destination_filepath_png, bucket_name=bucket_name)
    return




def download_image(url):
    # Fetch image data from the URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")
