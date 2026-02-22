import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
logo = soup.find('img', {'alt': 'Google'})
print(logo.get('src'))