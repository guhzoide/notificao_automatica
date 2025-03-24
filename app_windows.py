import time
import telebot
from datetime import datetime
from selenium import webdriver
from bin.setup import BOT_TOKEN, BOT_CHAT_ID, URL
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = Service('/bin/chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
navegador = webdriver.Chrome(service=chrome_driver, options=chrome_options)
navegador.get(URL)
bot=telebot.TeleBot(BOT_TOKEN)

print("==== Iniciando automacao ====")
now = datetime.now()
date_time = now.strftime("%d/%m/%Y | %H:%M:%S")
print(date_time)
chat_ids = BOT_CHAT_ID.items()
for chat in chat_ids:
    print(f"Enviando para: {chat[0]}")
    bot.send_message(chat[1], f"Iniciando automação {date_time}")

print("==== Fazendo login ====")
navegador.find_element(By.ID, 'input-14').send_keys("06004387916")
navegador.find_element(By.ID, 'input-18').send_keys("senha#conceitos")
lista_botoes = navegador.find_elements(By.CLASS_NAME, 'v-btn__content')

for botao in lista_botoes:
    if "Entrar" in botao.text:
        botao.click()
        break

while True:
    print("==== Verificando filtros ====")
    time.sleep(5)
    select_slots = navegador.find_elements(By.CLASS_NAME, "v-select__slot")
    for slot in select_slots:
        if "Pré filtros" in slot.text:
            slot.click()
            break

    print("==== Filtrando ====")
    time.sleep(1)
    navegador.find_element(By.XPATH, "//div[contains(text(), 'Telerradio')]").click()

    print("==== Listando status ====")
    time.sleep(5)
    lista_status = navegador.find_elements(By.CLASS_NAME, 'v-chip__content')
    contador = 0
    for status in lista_status:
        if "Aberto" in status.text:
            contador += 1
        else:
            pass

    if contador != 0:
        print(f"Existem {contador} exames pendentes")
        for chat in chat_ids:
            print(f"Enviando para: {chat[0]}")
            bot.send_message(chat[1], f"Iniciando automação {date_time}")

    time.sleep(1800)
    print("==== Refresh ====")
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y | %H:%M:%S")
    print(date_time)
    navegador.refresh()
