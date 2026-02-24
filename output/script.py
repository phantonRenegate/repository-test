#!/usr/bin/env python
import requests
def get_ui_patch(text):
    url = 'https://example.com/api/patch'
    response = requests.post(url, json={'text': text})
    return response.json()
