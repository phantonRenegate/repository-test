# Script to fetch UI patch from Google text box
import requests

def get_ui_patch(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f'Failed to fetch UI patch: {response.status_code}')