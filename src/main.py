import requests
from bs4 import BeautifulSoup

def get_google_logo_url():
    url = "https://www.google.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_tag = soup.find('img', {'class': 'lnXdpd'})
    if logo_tag and 'src' in logo_tag.attrs:
        return logo_tag['src']
    else:
        return None

if __name__ == '__main__':
    print(get_google_logo_url())