import json
from werkzeug.datastructures import ImmutableMultiDict
from flask import request
# import mock
from app.query import send_to_dropbox, check_async_status

from config import DROPBOX_TOKEN


def test_can_read_media_files(client):
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
    data = imd.to_dict(flat=False)

    res = client.post('/query/', data=data)
    
    assert res.status_code == 400

def test_can_throw_error_on_invalid_data(client):
    data = {}

    res = client.post('/query/', data=data)
    
    assert res.status_code == 400

