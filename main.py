from playwright_config import playwright_config

if __name__ == "__main__":
  ms_token_value = "TeSs7SDkNrm_kq35QSb_8JdLt_OiRC5yhxA0cHmr5m_EjgxvM2TZ7Ibi4UZbIM0A2UdltCHsRj4iPD7eJsJ0Y_f99D_32uJE8ht3w8arJHKnpXJzrJJoI99pospheb8w2BgnD-y6Ured4g=="

  browser = playwright_config().launch(headless=False)
  context = browser.new_context()
  context.add_cookies([{
    'name': 'msToken',
    'value': ms_token_value,
    'domain': '.tiktok.com',
    'path': '/',
    'httpOnly': False,
    'secure': True
  }, {
    'name': 'msToken',
    'value': ms_token_value,
    'domain': 'www.tiktok.com',
    'path': '/',
    'httpOnly': False,
    'secure': False
  }
])
  
  page = context.new_page()

  def handle_response(response):
    print(response)
    if "recommend/item_list" in response.url:
        print("Resposta da API:", response.json())


  page.on("response", handle_response)
  page.goto("https://tiktok.com")

  page.wait_for_timeout(5000)
  browser.close()