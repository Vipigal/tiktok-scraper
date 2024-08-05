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
		json_response = response.json()
		if("itemList" in json_response):
			print("Resposta da API:", response.json()["itemList"][0]["desc"])

if __name__ == "__main__":
	browser = playwright_config().launch(headless=False)
	try:
		context = browser.new_context()
		page = context.new_page()
		page.goto("https://tiktok.com")
		page.wait_for_timeout(2000)
		context.add_cookies(cookies)
		page.wait_for_timeout(2000)
		page.on("response", handle_response)
		page.goto("https://tiktok.com/foryou")
		page.wait_for_timeout(10000)
    
		browser.close()
		
	except Exception as e:
		print(e)
		browser.close()