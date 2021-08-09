import pytest
from flask import Flask, request

# import mock
from app.query import send_to_dropbox, make_filename, DROPBOX_URL, check_async_status

from config import DROPBOX_TOKEN

def test_check():
    assert True == True

def test_send_to_dropbox():
    media_url = "https://storage.googleapis.com/gd-wagtail-prod-assets/original_images/evolving_google_identity_3x2.jpg"
    media_type = "image/jpeg"
    resp = send_to_dropbox(media_url, media_type, DROPBOX_TOKEN)
    assert resp.status_code == 200
    data = resp.json()
    assert data['async_job_id']

def test_fails_async_status():
    resp = check_async_status('2')
    assert resp.status_code == 409
    data = resp.json()
    assert data['error']

def test_passes_async_status():
    media_url = "https://storage.googleapis.com/gd-wagtail-prod-assets/original_images/evolving_google_identity_3x2.jpg"
    media_type = "image/jpeg"
    resp = send_to_dropbox(media_url, media_type, DROPBOX_TOKEN)
    data = resp.json()
    async_job_id = data['async_job_id']
    resp = check_async_status(async_job_id)
    assert resp.status_code == 200
    data = resp.json()
    assert data['.tag'] == 'complete'

def test_make_filename():
    media_url = "https://original_images/test.jpg"
    media_type = "image/jpeg"
    filename = make_filename(media_url, media_type)
    assert filename == "test.jpeg"


