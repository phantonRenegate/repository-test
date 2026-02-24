# This script will request the Google homepage and extract the path to the Google logo.
import requests
from bs4 import BeautifulSoup

def get_google_logo_path():
    url = 'https://www.google.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_img_tag = soup.find('img', {'alt': 'Google'})
    if logo_img_tag:
        return logo_img_tag['src']
    else:
        return None