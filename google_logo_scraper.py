import requests
from bs4 import BeautifulSoup

url = 'https://www.google.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
logo_path = soup.find('img', {'class': 'lnXdpd'})['src']
print(logo_path)