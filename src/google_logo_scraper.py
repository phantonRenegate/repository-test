# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# URL of the Google logo on their homepage
url = 'https://www.google.com'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the image tag with the class containing the Google logo
logo_image = soup.find('img', {'class': 'lnXdpd'})

if logo_image:
    # Get the URL of the logo
    logo_url = logo_image['src']
    print(logo_url)
else:
    print('Google logo not found.')