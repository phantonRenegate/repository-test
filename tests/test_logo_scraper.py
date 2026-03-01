import unittest
from src.logo_scraper import get_google_logo_ui_patch
class TestLogoScraper(unittest.TestCase):
    def test_get_google_logo(self):
        img = get_google_logo_ui_patch()
        self.assertIsNotNone(img)
if __name__ == '__main__':
    unittest.main()