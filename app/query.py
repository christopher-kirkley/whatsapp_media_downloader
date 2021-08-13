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
    _from = values.get("From", '')
    profile_name = values.get("ProfileName", '')
    content_type = values.get(f"MediaContentType{i}", '')

    base_filename = url.split('/')[-1].split('.')[0] + '_' + body + '_' + _from.split('+')[-1] + '_' + profile_name

    filename = base_filename + '.' + content_type.split('/')[-1]

    return (url, filename) 

def send_to_dropbox(media_url, filename, DROPBOX_TOKEN):

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

    if media_files:
        for media_url, filename in media_files:
            resp = send_to_dropbox(media_url, filename, DROPBOX_TOKEN)
            job_id = resp.json()['async_job_id']
            resp = check_async_status(job_id)
            if resp.json()['.tag'] == 'in_progress':
                return jsonify({'error': 'malformed request'}), 400
            if res.json()['.tag'] == 'complete':
                return jsonify({'success': 'complete'}), 200

    content = {'error': 'missing whatsapp content'}
    return jsonify(content), 400


