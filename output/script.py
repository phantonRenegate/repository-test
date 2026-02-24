import requests

def fetch_ui_patch():
    url = "https://example.com/textbox"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch UI patch")