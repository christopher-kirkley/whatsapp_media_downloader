import json

import requests_mock
import requests

from werkzeug.datastructures import ImmutableMultiDict
from flask import request
# import mock
from app.query import send_to_dropbox, check_async_status

from config import DROPBOX_TOKEN


imd = ImmutableMultiDict(
        [('MediaContentType0', 'image/jpeg'),
        ('SmsMessageSid', 'MMefb5edf55ae1b57af359103b5a68f52a'),
        ('NumMedia', '1'),
        ('ProfileName', 'Me'),
        ('SmsSid', 'MMefb5edf55ae1b57af359103b5a68f52a'),
        ('WaId', '15039365678'), ('SmsStatus', 'received'),
        ('Body', 'caption'),
        ('To', 'whatsapp:+15553333333'),
        ('NumSegments', '1'),
        ('MessageSid', 'MMefb5edf55ae1b57af359103b5a68f52a'),
        ('AccountSid', 'AC689400cfde1ea75d3932b56f84fff41c'),
        ('From', 'whatsapp:+15559999999'),
        ('MediaUrl0', 'https://api.twilio.com/2010-04-01/Accounts/AC689400cfde1ea75d3932b56f84fff41c/Messages/MMefb5edf55ae1b57af359103b5a68f52a/Media/randomstring'),
        ('ApiVersion', '2010-04-01')]
        )

def test_can_read_media_files(client):
    data = imd.to_dict(flat=False)

    res = client.post('/query/', data=data)
    
    assert res.status_code == 200

def test_can_throw_error_on_invalid_data(client):
    data = {}

    res = client.post('/query/', data=data)
    
    assert res.status_code == 400

def test_mock_send_to_dropbox_with_error(requests_mock, client):

    # set up mock data

    save_url = "https://api.dropboxapi.com/2/files/save_url"
    content = {'.tag': 'async_job_id', 'async_job_id': 1}
    requests_mock.post(save_url, json=content)

    check_url = "https://api.dropboxapi.com/2/files/save_url/check_job_status"
    content = {'.tag': 'in_progress', 'async_job_id': 1}
    requests_mock.post(check_url, json=content)

    data = imd.to_dict(flat=False)

    res = client.post('/query/', data=data)

    assert res.status_code == 200
    # assert json.loads(res.data) == {'error': 'malformed request'}

def test_mock_send_to_dropbox_completes(requests_mock, client):

    # set up mock data

    save_url = "https://api.dropboxapi.com/2/files/save_url"
    content = {'.tag': 'async_job_id', 'async_job_id': 1}
    requests_mock.post(save_url, json=content)

    check_url = "https://api.dropboxapi.com/2/files/save_url/check_job_status"
    content = {'.tag': 'complete', 'async_job_id': 1}
    requests_mock.post(check_url, json=content)

    data = imd.to_dict(flat=False)

    res = client.post('/query/', data=data)

    assert res.status_code == 200
    # assert json.loads(res.data) == {'success': 'complete'}

def test_mock_send_to_dropbox_invalid_url(requests_mock, client):

    # set up mock data

    save_url = "https://api.dropboxapi.com/2/files/save_url"
    content = {
        "error_summary": "other/...",
        "error": {
            ".tag": "other"
        }
    }
    requests_mock.post(save_url, json=content)

    check_url = "https://api.dropboxapi.com/2/files/save_url/check_job_status"
    content = {'.tag': 'complete', 'async_job_id': 1}
    requests_mock.post(check_url, json=content)

    data = imd.to_dict(flat=False)

    res = client.post('/query/', data=data)

    assert res.status_code == 400
    assert json.loads(res.data) == {'error': 'dropbox error'}

def test_send_to_dropbox(requests_mock):
    # set up mock data

    save_url = "https://api.dropboxapi.com/2/files/save_url"
    content = {'.tag': 'async_job_id', 'async_job_id': 1}
    requests_mock.post(save_url, json=content)

    media_url = "https://storage.googleapis.com/gd-wagtail-prod-assets/original_images/evolving_google_identity_3x2.jpg"
    filename = 'test.jpg'
    resp = send_to_dropbox(media_url, filename, DROPBOX_TOKEN)
    assert resp.status_code == 200
    data = resp.json()
    assert data['async_job_id']

