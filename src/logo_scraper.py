import requests
from io import BytesIO
from PIL import Image

def get_google_logo_ui_patch():
    url = 'https://www.google.com/logos/doodles/2023/google-100th-logo-doodle-6987452232226880.4-ltr.png'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img