import os
from dotenv import load_dotenv
from botocore.config import Config
from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
from chalicelib import extraction_service
from chalicelib import contact_store

import base64
import json

# Get environment variable
load_dotenv()
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
S3_BUCKET = os.environ['S3_BUCKET']
DB_TABLE = os.environ['DB_TABLE']

# chalice app configuration
app = Chalice(app_name='Capabilities')
app.debug = True

# credential and config setup
config = {
    "ACCESS_KEY": ACCESS_KEY,
    "SECRET_KEY": SECRET_KEY,
    "boto3_config": Config(
        region_name='us-east-2'
    )
}

# services initialization
storage_location = S3_BUCKET
storage_service = storage_service.StorageService(
    storage_location, config)
recognition_service = recognition_service.RecognitionService(
    storage_location, config)
extraction_service = extraction_service.ExtractionService(
    config)
store_location = DB_TABLE
contact_store = contact_store.ContactStore(
    store_location, config)


@app.route('/images/{image_id}/extract-info', methods=['POST'], cors=True)
def extract_image_info(image_id):
    MIN_CONFIDENCE = 70

    text_lines = recognition_service.detect_text(image_id)

    contact_lines = []
    for line in text_lines:
        # check confidence
        if float(line['confidence']) >= MIN_CONFIDENCE:
            contact_lines.append(line['text'])

    contact_string = '   '.join(contact_lines)
    contact_info = extraction_service.extract_contact_info(contact_string)

    return contact_info


@app.route('/contacts', methods=['POST'], cors=True)
def save_contact():
    request_data = json.loads(app.current_request.raw_body)

    contact = contact_store.save_contact(request_data)

    return contact


@app.route('/contacts/{search_name}', methods=['GET'], cors=True)
def get_contacts(search_name):
    contacts = contact_store.get_contacts(search_name)

    return contacts


@app.route('/images', methods=['POST'], cors=True)
def upload_image():
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)

    return image_info
