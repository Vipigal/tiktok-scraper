from playwright_config import playwright_config
import asyncio
from db_connect import db_connect
from db_config import load_config
import os
from agents import classificar_conteudo
from repository import TiktokRepository

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

	# cookies = [
	# 	{
	# 		'name': 'sessionid',
	# 		'value': 'a4953df344fba92a7717508eeb04ae89',
	# 		'domain': '.tiktok.com',
	# 		'path': '/',
	# 		'httpOnly': False,
	# 		'secure': True
	# 	}
	# ]
	# videos:dict = {}

	# async def handle_response(response):
	# 	if "recommend/item_list" in response.url:
	# 		json_response = await response.json()
	# 		if("itemList" in json_response):
	# 			videoList = json_response["itemList"]
	# 			for video in videoList:
	# 				videos[video["id"]] = video

	# videos_assistidos = 0
	# browser = await playwright_config().launch(headless=False)
  try:
    repository = TiktokRepository()
    if repository.test_has_data():
      print("Banco de dados ja possui dados dos videos.")
    else:
      print("Banco de dados esta vazio. Inicializando tabela de videos...")
      repository.create_videos_table()
      
    repository.insertTiktokData("123456", "descricao teste", "hashtag1 hashtag2")

    print("Dados inseridos com sucesso.")

    print("Videos Salvos: ", repository.get_all())


    repository.close()

	# 	context = await browser.new_context()
	# 	page = await context.new_page()
	# 	await page.goto("https://tiktok.com")
	# 	await page.wait_for_timeout(2000)
	# 	await context.add_cookies(cookies)
	# 	await page.wait_for_timeout(2000)
	# 	await page.goto("https://tiktok.com/foryou")
	# 	page.on("response", lambda response: asyncio.create_task(handle_response(response)))
	# 	await page.wait_for_timeout(2000)

	# 	await page.click(".tiktok-web-player")
	# 	await page.wait_for_timeout(2000)

	# 	print("[INFO] Iniciando a execução do script...")

	# 	while videos_assistidos < 20:
	# 		await page.wait_for_timeout(2000)
	# 		print("[INFO] Extracao de dados do video...")
	# 		video_url = page.url
	# 		video_id = extract_video_id(video_url)
	# 		if(video_id in videos):
	# 			video_data = videos[video_id]
	# 			if("desc" in video_data and video_data["desc"] != ""):
	# 				print("[DATA] Descrição do Vídeo:", video_data["desc"]) #analisar se descrição encaixa no tema escolhido aqui

	# 			hashtags = get_video_hashtags(video_data)
	# 			if len(hashtags) > 0:
	# 				print("[DATA] Hashtags do Vídeo:", " ".join(hashtags)) #analisar se hashtags encaixam no tema escolhido aqui
					
	# 			classificacao = classificar_conteudo(video_data["desc"], hashtags)
	# 			print(classificacao)

	# 		print("[INFO] Assistindo ao vídeo (20 segundos)...")
	# 		await page.wait_for_timeout(20000)
	# 		print("[INFO] Vídeo assistido! Pulando para o proximo vídeo...")
	# 		videos_assistidos = videos_assistidos + 1
	# 		print("[INFO] Vídeos assistidos:", videos_assistidos)
	# 		await page.click("[data-e2e='arrow-right']")

	# 	await browser.close()
		
  except Exception as e:
    print("[ERRO]", e)
		# await browser.close()


if __name__ == "__main__":
  os.environ["OPENAI_API_KEY"] = "NA"
  os.environ['OPENAI_API_BASE']='http://localhost:11434'
  os.environ['OPENAI_MODEL_NAME']='llama2'
  os.environ['OPENAI_API_KEY']=''
  try:
    asyncio.run(main())
  except Exception as e:
    print("[ERRO]", e)
    exit(1)