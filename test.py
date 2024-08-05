from playwright_config import playwright_config

cookies = [
    {
        'name': 'sessionid',
        'value': 'a4953df344fba92a7717508eeb04ae89',
        'domain': '.tiktok.com',
        'path': '/',
        'httpOnly': False,
        'secure': True
    }
]

def handle_response(response):
	if "recommend/item_list" in response.url:
		print("Resposta da API:", response.json().itemList[0].desc)

if __name__ == "__main__":
	try:
		browser = playwright_config().launch(headless=False)
		context = browser.new_context()
		page = context.new_page()
		page.goto("https://tiktok.com")
		page.wait_for_timeout(2000)
		context.add_cookies(cookies)
		page.wait_for_timeout(2000)
		page.reload()
		page.wait_for_timeout(10000)
    
		page.on("response", handle_response)
		browser.close()
		
	except Exception as e:
		print(e)
		browser.close()