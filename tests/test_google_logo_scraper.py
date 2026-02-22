import unittest
from src.google_logo_scraper import get_google_logo_url
class TestGoogleLogoScraper(unittest.TestCase):
    def test_get_google_logo_url(self):
        url = 'https://www.google.com'
        expected_logo_url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_274x91dp.png'
        self.assertEqual(get_google_logo_url(url), expected_logo_url)
def main():
    unittest.main()
if __name__ == '__main__':
    main()