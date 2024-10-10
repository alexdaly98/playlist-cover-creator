import os
from dotenv import load_dotenv
from google.cloud import secretmanager, storage
import json

load_dotenv()

# Charger les variables d'environnement locales
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérifier si on est en environnement de production (GCP)
if os.getenv("GOOGLE_CLOUD_ENV") == "production":
    # Instancier le client Secret Manager
    client = secretmanager.SecretManagerServiceClient()
    
    # Accéder aux secrets
    secret_name = "projects/playlist-cover-creator/secrets/GOOGLE_APPLICATION_CREDENTIALS/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    service_account_info = response.payload.data.decode("UTF-8")
    service_account_json = json.loads(service_account_info)
    
    # Authentifier les clients Google Cloud avec les informations d'identification
    storage_client = storage.Client.from_service_account_info(service_account_json)
else:
    # Utiliser les informations d'identification locales pour le développement
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "playlist-cover-creator-9d9325a23f53.json"
