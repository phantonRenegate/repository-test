#!/usr/bin/env python3
import requests
def get_google_logo_ui_patch():
    url = 'https://www.google.com/logos/logo.png'
    response = requests.get(url)
    if response.status_code == 200:
        with open('logo.png', 'wb') as file:
            file.write(response.content)
    else:
        print(f'Failed to fetch logo: {response.status_code}')