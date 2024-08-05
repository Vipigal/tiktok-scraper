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

videos:dict = {}

def handle_response(response):
	if "recommend/item_list" in response.url:
		json_response = response.json()
		if("itemList" in json_response):
			videoList = json_response["itemList"]
			for video in videoList:
				videos[video["id"]] = video


def extract_video_id(url):
    return url.split('/')[-1]

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

		page.click(".tiktok-web-player")
		page.wait_for_timeout(20000)

		video_url = page.url
		video_id = extract_video_id(video_url)

		video_data = videos[video_id]
		print("ID do Vídeo:", video_id)

		print("Descrição do Vídeo:", video_data["desc"])
    
		browser.close()
		
	except Exception as e:
		print(e)
		browser.close()