from flask import Flask, request, send_file
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from pathlib import Path
import io
import json

from config import DROPBOX_KEY, DROPBOX_SECRET, DROPBOX_TOKEN

app = Flask(__name__)

def send_to_dropbox(item):
    media_url, media_type = item

    filename = media_url.split('/')[-1] + '.' + media_type.split('/')[-1]

    dropbox_url = "https://api.dropboxapi.com/2/files/save_url"

    body = {
        "path": f"/WhatsAppMedia/{filename}",
        "url": media_url
    }

    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(dropbox_url, headers=headers, data=json.dumps(body))

    return 0

@app.route('/', methods=['POST'])
def get_media():
    message_sid = request.values.get('MessageSid', '')
    from_number = request.values.get('From', '')
    num_media = int(request.values.get('NumMedia', 0))

    media_files = [(request.values.get(f"MediaUrl{i}", ''),
                    request.values.get(f"MediaContentType{i}", ''))
                   for i in range(0, num_media)]

    for item in media_files:
        send_to_dropbox(item)

    return 'success'

if __name__ == '__main__':
    app.run()
