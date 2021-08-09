from flask import Flask, request, Blueprint
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json

from config import DROPBOX_KEY, DROPBOX_SECRET, DROPBOX_TOKEN

query = Blueprint('query', __name__, url_prefix='/query')

DROPBOX_URL = ""

def make_filename(media_url, media_type):
    filename = media_url.split('/')[-1].split('.')[0] + '.' + media_type.split('/')[-1]
    return filename

def send_to_dropbox(media_url, media_type, DROPBOX_TOKEN):
    filename = make_filename(media_url, media_type)

    body = {
        "path": f"/{filename}",
        "url": media_url
    }

    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.dropboxapi.com/2/files/save_url", headers=headers, data=json.dumps(body))

    return response

def check_async_status(async_job_id):
    body = {
        "async_job_id": async_job_id
    }

    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.dropboxapi.com/2/files/save_url/check_job_status", headers=headers, data=json.dumps(body))

    return response

@query.route('/', methods=['POST'])
def get_media():
    num_media = int(request.values.get('NumMedia', 0))

    media_files = [(request.values.get(f"MediaUrl{i}", ''),
                    request.values.get(f"MediaContentType{i}", ''))
                   for i in range(0, num_media)]

    for media_url, media_content in media_files:
        send_to_dropbox(media_url, media_content, DROPBOX_TOKEN)

    return 'success'

@query.route('/hi', methods=["GET"])
def hello():
    return json.dumps('hi')
