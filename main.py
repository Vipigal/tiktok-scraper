from playwright_config import playwright_config
import asyncio


def extract_video_id(url):
    return url.split('/')[-1]

def get_video_hashtags(video_data):
	hashtags = []
	if "challenges" not in video_data:
		return hashtags
	
	for hashtag in video_data["challenges"]:
		hashtags.append(hashtag["title"])
	return hashtags


async def main():
	
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

	async def handle_response(response):
		if "recommend/item_list" in response.url:
			json_response = await response.json()
			if("itemList" in json_response):
				videoList = json_response["itemList"]
				for video in videoList:
					videos[video["id"]] = video

	videos_assistidos = 0
	browser = await playwright_config().launch(headless=False)
	try:
		context = await browser.new_context()
		page = await context.new_page()
		await page.goto("https://tiktok.com")
		await page.wait_for_timeout(2000)
		await context.add_cookies(cookies)
		await page.wait_for_timeout(2000)
		page.on("response", lambda response: asyncio.create_task(handle_response(response)))
		await page.goto("https://tiktok.com/foryou")
		await page.wait_for_timeout(2000)

		await page.click(".tiktok-web-player")
		await page.wait_for_timeout(2000)

		print("Iniciando a execução do script")

		while videos_assistidos < 20:
			await page.wait_for_timeout(2000)
			print("Extracao de dados do video")
			video_url = page.url
			video_id = extract_video_id(video_url)
			if(video_id in videos):
				video_data = videos[video_id]
				print("ID do Vídeo:", video_id)
				if("desc" in video_data):
					print("Descrição do Vídeo:", video_data["desc"])
				print("oi")

				hashtags = get_video_hashtags(video_data)
				if len(hashtags) > 0:
					print("Hashtags do Vídeo:", " ".join(hashtags))

			print("Assistindo ao vídeo")
			await page.wait_for_timeout(20000)
			print("Vídeo assistido")
			videos_assistidos = videos_assistidos + 1
			print("Vídeos assistidos:", videos_assistidos)
			await page.click("[data-e2e='arrow-right']")

		await browser.close()
		
	except Exception as e:
		print(e)
		await browser.close()


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except Exception as e:
		print(e)
		print("Erro ao executar o script")
		exit(1)