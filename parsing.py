#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
from argparse import ArgumentParser  
import telegram
import threading
import time
import json
import glob
from telegram import InputMediaPhoto

TOKEN = '6380395533:AAE7POJ1Jznc7nSbwjJOGAyiH9bzPCde_Kc'
chat_id = "-1001924241753"
#keysearch = "сноуборд"
url = "https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated"
#payload = {"cat":"1010", "typ": "let", "rng": "6", "ar": "18", "prc": "r:20000,35000", "cur": "BYR", "rms": }
#jparams = '{"cat":"1010","typ":"let","rgn":"6","ar":"18","prc":"r:20000,35000","cur":"BYR","rms":"v.or:1,2","rnt":"1","sort":"lst.d","size":"42"}'
jparams = '{"cat":"2010","cur":"BYR","sort":"lst.d","size":"200"}'
payload = json.loads(jparams)

arrIds = []
global jsonStr
def writeIdsFile():
    for file in glob.glob('./*.txt'):
        arrIds.append(file.replace('.txt', '').replace('.\\', ''))
    jsonStr = json.dumps(arrIds)
    with open("ids.json", 'w') as f:
        f.write(jsonStr)
def addIdFile(id):
    ids = readIdsFile()
    ids.append(id)
    jsonStr = json.dumps(ids)
    with open("ids.json", 'w') as f:
        f.write(jsonStr)
def readIdsFile():
    with open('ids.json', 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
    return fcc_data
def findIdFile(id):
    file = readIdsFile()
    if id in file:
      print('уже есть')
      return 1
    else:
      print('еще нет')
      return 0
def get_photo(link):
  # парсинг фотографий и описания
  photo_link = []
  description = 'Описание не найдено'
  a = requests.get(link)
  try:

    soup_photo = bs(a.content, "html.parser")
    #print(soup_photo)
    soup_find_all = soup_photo.find("div", class_="swiper-zoom-container")
    soup_find_all_photo = soup_find_all.findAll("img", limit=9)
    #print(soup_photo)
    for photo in soup_find_all_photo:
      if photo["src"] not in photo_link:
        print(photo["src"])
        photo_link.append(photo["src"])
    description = soup_photo.find("div", itemprop="description").text
    if len(description) > 512:
      description = description[:509] + "..."
    
  except: pass
  return photo_link, description       

def get_api():
  # Запрос к APi и парсинг параметров
  try:
    r = requests.get(url, params=payload)
    result = r.json()

    for ads in result['ads']:
      link = ads['ad_link']
      names = ads['subject']
      idK = ads['ad_id']
      #for param in ads['ad_parameters']:
      #  if param['pl']
      if int(ads['price_usd']) != 0:
        price = int(ads['price_usd']) / 100
      else: price = "Договорная"
    return idK, link, names, price
  except: pass
  

def find_file(idK):
  try:
    file2 = open(idK + '.txt')
  except IOError as e:
    print(u'пока нет')
    return 0
  else:
    with file2:
      print(u'уже существует')
  return 1

def main():

  url = "https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated"
  jparams = '{"cat":"2010","cur":"BYR","sort":"lst.d","size":"20"}'
  payload = json.loads(jparams)
  try:
    r = requests.get(url, params=payload)
    result = r.json()

    for ads in result['ads']:
      media_group = []
      link = ads['ad_link']
      names = ads['subject']
      idK = ads['ad_id']
      params = ''
      for param in ads['ad_parameters']:
        if param['pu'] == 'ar':
          params = params + 'Город / Район: #' + param['vl'] + "\n"
          if param['pu'] == 'rgn':
            params = params + 'Область: #' + param['vl'] + "\n"
        if param['pu'] == 'brn':
          params = params + 'Марка: #' + param['vl'] + "\n"
        if param['pu'] == 'crl':
          params = params + 'Модель: #' + param['vl'] + "\n"
        if param['pu'] == 'mlg':
          params = params + 'Пробег: ' + param['vl'] + "\n"
        if param['pu'] == 'rgd':
          params = params + 'Год: #' + param['vl'] + "\n"
        if param['pu'] == 'crca':
          params = params + 'Объем: ' + param['vl'] + "\n"
        if param['pu'] == 'crg':
          params = params + 'Коробка передач: ' + param['vl'] + "\n"
        if param['pu'] == 'cre':
          params = params + 'Тип двигателя: #' + param['vl'] + "\n"

      if int(ads['price_usd']) != 0:
        price = int(ads['price_usd']) / 100
      else:
        price = "Договорная"
      check = findIdFile(str(idK))
      print(names)
      file = f'Объявление: {names}\nЦена: ${price}\n{params}'
      print(file)


      # Запись в файл для сравнения. отправка сообщения.

      if check == 0:
        if get_photo(link):
          for number, url in enumerate(get_photo(link)[0]):
            if number == 0:
              media_group.append(InputMediaPhoto(media=url, parse_mode='HTML', caption=file + "<a href='" + link + "'>Ссылка</a>\nОписание: " + get_photo(link)[1]))
            #media_group.append(InputMediaPhoto(media=url))
            if number == 4:
              break
        #print(media_group)
        addIdFile(str(idK))
        if len(media_group):
          try:
            bot.send_media_group(chat_id=chat_id, media=media_group)
          except:
            bot.send_message(text=file + link, chat_id=chat_id)
          print(u'отправлено без фото')
        else:
          bot.send_message(text=file + link, chat_id=chat_id)
          print(u'отправлено с фото')
        print(link)
        time.sleep(3)
        #bot.send_message(chat_id, f'Объявление: {names}, Цена: ${price} , {link}')
        #else:
        #  if not (price - 1 < float(t.split('Цена: ')[1]) < price + 1):
        #    if len(media_group):
        #      bot.send_media_group(chat_id=chat_id, media=media_group)
        #    else: bot.send_message(text=file + link, chat_id=chat_id)
  except Exception as e:
    bot.send_message(chat_id, e)
  threading.Timer(60.0, main).start()
    

bot = telegram.Bot(TOKEN)
main()
while True:
    try:
        bot.polling(none_stop=True, interval=5)
    except:
        pass