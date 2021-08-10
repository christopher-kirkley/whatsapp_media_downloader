
# import mock
from app.query import send_to_dropbox, check_async_status

from config import DROPBOX_TOKEN

def test_send_to_dropbox():
    media_url = "https://storage.googleapis.com/gd-wagtail-prod-assets/original_images/evolving_google_identity_3x2.jpg"
    filename = 'test.jpg'
    resp = send_to_dropbox(media_url, filename, DROPBOX_TOKEN)
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
    media_url = ''
    filename = 'test.jpg'
    resp = send_to_dropbox(media_url, filename, DROPBOX_TOKEN)
    data = resp.json()
    assert data == ''
    async_job_id = data['async_job_id']
    resp = check_async_status(async_job_id)
    assert resp.status_code == 200
    data = resp.json()
    assert data['.tag'] == 'complete'

    
