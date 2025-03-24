from playwright.sync_api import sync_playwright


class Scrapper:
    def __init__(self):
        self.browser = sync_playwright().start().chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.close()
        print("Browser closed")
