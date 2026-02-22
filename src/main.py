import requests
from bs4 import BeautifulSoup

def get_google_logo_path():
    url = 'https://www.google.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_img = soup.find('img', {'class': 'lnXdpd'})
    return logo_img['src']