# import mock
from app.query import make_filename

def test_make_filename():
    media_url = "https://original_images/test.jpg"
    media_type = "image/jpeg"
    filename = make_filename(media_url, media_type)
    assert filename == "test.jpeg"


def test_can_get_job_id_from_resp():
    mock_resp =  {'.tag': 'async_job_id', 'async_job_id': '6oNouvKk3NAAAAAAAAAAAQ'}
    async_job_id = get_job_id(mock_resp)
    assert async_job_id == '6oNouvKk3NAAAAAAAAAAAQ'

