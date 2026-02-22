import requests
from bs4 import BeautifulSoup

def get_google_logo_path():
    url = "https://www.google.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_img = soup.find('img', {'class': 'lnXdpd'})
    if logo_img and 'src' in logo_img.attrs:
        return logo_img['src']
    else:
        return None

if __name__ == "__main__":
    print(get_google_logo_path())