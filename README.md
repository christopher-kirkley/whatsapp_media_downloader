# WhatsApp Media Downloader

A Flask microservice that connects a WhatsApp number to Dropbox.

## Dependencies

- Flask
- Requests
- Twilio
- Pytest (optional)

## Setup

Requires creation of a file 'config.py' in project root that contains the following variables:

- DROPBOX_KEY
- DROPBOX_SECRET
- DROPBOX_TOKEN

## Usage

To set up, you will need a verified WhatsApp business Twilio account. You can optionally play with the Twilio sandbox for testing.

You'll also need to create an app for Dropbox API v2.

In the Twilo console, set the message receipient to your hosted app, with the '/query' endpoint.

Any message sent to the WhatsApp number will be forwarded to the Flask endpoint as data in a POST request. The media is stripped and renamed according to convention: unique_id:caption:senders_number:senders_name.extension

Media is processed and saved in the Dropbox folder /WhatsAppMedia
