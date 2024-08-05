from playwright.async_api import async_playwright

class playwright_config:
    def __init__(self):
        self.playwright = async_playwright()
  
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.playwright.__exit__(exc_type, exc_val, exc_tb)

    async def launch(self, headless=True):
          instance = await self.playwright.start()
          chromium = instance.chromium
          browser = await chromium.launch(headless=headless)
           
          return browser

print("Config Loaded!")