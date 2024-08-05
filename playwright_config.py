from playwright.sync_api import sync_playwright, Playwright

class playwright_config:
    def __init__(self):
        self.playwright = sync_playwright()
  
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.playwright.__exit__(exc_type, exc_val, exc_tb)

    def launch(self, headless=True):
          chromium = self.playwright.start().chromium # or "firefox" or "webkit".
          browser = chromium.launch(headless=headless)
           
          return browser

print("Config Loaded!")