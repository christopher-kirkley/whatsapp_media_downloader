from _pytest.config import filename_arg
from flask import Flask, request, Blueprint, jsonify
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json

from config import DROPBOX_KEY, DROPBOX_SECRET, DROPBOX_TOKEN

query = Blueprint('query', __name__, url_prefix='/query')

DROPBOX_URL = ""


def make_file_tuple(i, values):
    url = values.get(f"MediaUrl{i}", '')
    body = values.get("Body", '')
    _from = values.get("From", '').split('+')[-1]
    profile_name = values.get("ProfileName", '')
    content_type = values.get(f"MediaContentType{i}", '')

    filename = url.split('/')[-1].split('.')[0] + '_' + body + '_' + _from + '_' + profile_name + '.' + content_type.split('/')[-1]

    return {'url': url, 'filename': filename, '_from': _from}

def send_to_dropbox(item, DROPBOX_TOKEN):

    # sends media url to dropbox api endpoint
    # constructs the file path to a subdirectory, storing media by contacts telephone number
    

    media_url = item.get('url')
    _path = item.get('_from') + '/' + item.get('filename') 
    

    body = {
        "path": f"/{_path}",
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

@query.route('/', methods=['GET'])
def hi():
    return str('hi')

@query.route('/', methods=['POST'])
def get_media():

    try:
        num_media = int(request.values.get('NumMedia'), 0)
    except TypeError:
        content = {'error': 'invalid whatsapp content'}
        return jsonify(content), 400

    media_files = [ make_file_tuple(i, request.values) for i in range(0, num_media)]

    if media_files == []:
        content = {'error': 'missing whatsapp content'}
        return jsonify(content), 400

    for item in media_files:
        resp = send_to_dropbox(item, DROPBOX_TOKEN)
        if resp.json().get('error'):
            content = {'error': 'dropbox error'}
            return jsonify(content), 400
        job_id = resp.json().get('async_job_id')
        resp = check_async_status(job_id)
        twilio_resp = MessagingResponse()
        if resp.json().get('.tag') == 'in_progress':
            return str(twilio_resp), 200
        if resp.json()['.tag'] == 'complete':
            return str(twilio_resp), 200

