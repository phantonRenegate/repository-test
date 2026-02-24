#!/usr/bin/env python3
import requests
def get_google_ui_patch(text):
    url = 'https://example.com/api/ui-patch'
    response = requests.post(url, data={'text': text})
    return response.text