# import mock
from app.query import make_file_tuple

def test_make_filename():
    media_url = "https://original_images/test.jpg"
    values = {
            "MediaUrl0" : 'https://www.google.com/qwerty',
            "Body": 'caption',
            "From": '+19995555555',
            "ProfileName": "Bobo",
            "MediaContentType0": "image/jpeg",
            }
    filename = make_file_tuple(0, values)
    assert filename == ("https://www.google.com/qwerty", "qwerty_caption_19995555555_Bobo.jpeg")


