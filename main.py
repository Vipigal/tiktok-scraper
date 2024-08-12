from playwright_config import playwright_config
import asyncio
import os
from agents import classificar_conteudo
from repository import TiktokRepository
import json
import time
from datetime import datetime


def export_to_json(rows, description, output_file):
    # Obter os nomes das colunas
    columns = [desc[0] for desc in description]

    # Converter os dados para um formato serializável em JSON
    data = []
    for row in rows:
        row_dict = {}
        for col, val in zip(columns, row):
            if isinstance(val, datetime):
                row_dict[col] = val.isoformat()  # Converter datetime para string
            else:
                row_dict[col] = val
        data.append(row_dict)

    # Serializar os dados para JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def extract_video_id(url):
    return url.split("/")[-1]


def get_video_hashtags(video_data):
    hashtags = []
    if "challenges" not in video_data:
        return hashtags

    for hashtag in video_data["challenges"]:
        hashtags.append(hashtag["title"])
    return hashtags


def get_video_stickerText(video_data):
    stickerTexts = []
    if "stickersOnItem" not in video_data:
        return stickerTexts

    for stickerText in video_data["stickersOnItem"]:
        stickerTexts.append(stickerText["stickerText"][0])
    return stickerTexts


async def main():
    account_name = "vinicius"
    try:
        cookies = [
            {
                "name": "sessionid",
                "value": "a4953df344fba92a7717508eeb04ae89",
                "domain": ".tiktok.com",
                "path": "/",
                "httpOnly": False,
                "secure": True,
            }
        ]

        videos: dict = {}

        async def handle_response(response):
            if "recommend/item_list" in response.url:
                json_response = await response.json()
                if "itemList" in json_response:
                    videoList = json_response["itemList"]
                    for video in videoList:
                        videos[video["id"]] = video

        videos_assistidos = 0
        print("[INFO] Inicializando o playwright...")
        browser = await playwright_config().launch(headless=False)

        print("[INFO] Inicializando o banco de dados...")
        repository = TiktokRepository()

        if repository.test_has_data():
            print("[INFO] Banco de dados ja foi inicializado.")
        else:
            print(
                "[INFO] Banco de dados nao esta inicializado. Configurando tabelas..."
            )
            repository.create_videos_table()

        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://tiktok.com")
        await page.wait_for_timeout(2000)
        await context.add_cookies(cookies)
        await page.wait_for_timeout(2000)
        await page.goto("https://tiktok.com/foryou")
        page.on(
            "response", lambda response: asyncio.create_task(handle_response(response))
        )

        comment_span = page.locator("[data-e2e='comment-icon']").first
        await comment_span.wait_for(state="visible")
        comment_button = comment_span.locator("..")
        await comment_button.click()

        # await comment_button.click(".tiktok-web-player")

        print("[INFO] Iniciando a execução do script...")

        while videos_assistidos < 20:
            start_time = time.time()

            await page.wait_for_timeout(2000)
            print("[INFO] Extracao de dados do video...")
            video_url = page.url
            video_id = extract_video_id(video_url)
            if video_id in videos:
                video_data = videos[video_id]
                description = None

                if "isAd" in video_data and video_data["isAd"] == True:
                    print("[INFO] Video é um anúncio. Pulando...")
                    await page.click("[data-e2e='arrow-right']")
                    continue

                if "desc" in video_data and video_data["desc"] != "":
                    description = video_data["desc"]
                    print("[DATA] Descrição do Vídeo:", video_data["desc"])

                hashtags = get_video_hashtags(video_data)
                hashtags_string = " ".join(f"#{tag}" for tag in hashtags)
                if len(hashtags) > 0:
                    print("[DATA] Hashtags do Vídeo:", " ".join(hashtags))

                stickerTexts = get_video_stickerText(video_data)
                stickerTexts_string = " ".join(
                    f"{stickerText}" for stickerText in stickerTexts
                )
                if len(stickerTexts) > 0:
                    print("[DATA] StickerTexts do Vídeo:", stickerTexts_string)

                if (
                    (description is None or description == "")
                    and len(hashtags) == 0
                    and len(stickerTexts) == 0
                ):
                    print(
                        "[INFO] Video não possui conteudo a ser analisado. Pulando..."
                    )
                    await page.click("[data-e2e='arrow-right']")
                    continue

                classificacao = await classificar_conteudo(
                    description, hashtags, stickerTexts_string
                )
                liked = False
                print(classificacao)
                if "True" in str(classificacao) or "true" in str(classificacao):
                    # like video
                    like_span = page.locator("[data-e2e='browse-like-icon']").first
                    await like_span.wait_for(state="visible")
                    like_button = like_span.locator("..")
                    await like_button.click()
                    liked = True
                    print(
                        "[INFO] Video faz parte de Echo Chamber. Curtindo e Assistindo ao vídeo (35 segundos)..."
                    )
                    await page.wait_for_timeout(35000)
                else:
                    print(
                        "[INFO] Video não faz parte Echo Chamber. Não será curtido. Pulando..."
                    )

                end_time = time.time()

                # Calcula o tempo total em segundos
                watch_time = end_time - start_time

                repository.add_tiktok(
                    video_id,
                    video_data["desc"] or None,
                    hashtags_string or None,
                    classificacao,
                    liked,
                    f"{int(watch_time)}s",
                    account_name,
                    videos_assistidos + 1,
                )

            print("[INFO] Vídeo assistido! Pulando para o proximo vídeo...")
            videos_assistidos = videos_assistidos + 1
            print("[INFO] Vídeos assistidos:", videos_assistidos)
            await page.click("[data-e2e='arrow-right']")

        print("[INFO] Script finalizado e dados coletados com sucesso.")
        [collected_data, description] = repository.get_all()
        print("[DATA] Videos Salvos ate agora: ", len(collected_data))
        # Save collected_data as JSON
        export_to_json(collected_data, description, "result.json")

        await browser.close()
        repository.close()

    except Exception as e:
        print("[ERRO]", e)
        await browser.close()
        repository.close()


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "NA"
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
    os.environ["OPENAI_MODEL_NAME"] = "llama2"
    os.environ["OPENAI_API_KEY"] = ""
    try:
        print("[INFO] Iniciando a execução do script...")
        asyncio.run(main())
    except Exception as e:
        print("[ERRO]", e)
        exit(1)
