import requests
import threading
import json
import time
import telegram
from telegram import InputMediaPhoto

token = "6380395533:AAE7POJ1Jznc7nSbwjJOGAyiH9bzPCde_Kc"
print("create bot")
bot = telegram.Bot(token)
print("created")
url = "https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated"
#payload = {"cat":"1010", "typ": "let", "rng": "6", "ar": "18", "prc": "r:20000,35000", "cur": "BYR", "rms": }
#jparams = '{"cat":"1010","typ":"let","rgn":"6","ar":"18","prc":"r:20000,35000","cur":"BYR","rms":"v.or:1,2","rnt":"1","sort":"lst.d","size":"42"}'
jparams = '{"cat":"2010","rgn":"2","cur":"BYR","sort":"lst.d","size":"42"}'
payload = json.loads(jparams)
user_id = '244368533'


def get_photo(link):
    # парсинг фотографий и описания
    photo_link = []
    description = 'Описание не найдено'
    a = requests.get(link)
    try:
        soup_photo = bs(a.content, "html.parser")
        soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__FY9R4", limit=9)
        for photo in soup_find_all_photo:
            if photo["src"] not in photo_link:
                photo_link.append(photo["src"])
        description = soup_photo.find("div", itemprop="description").text
        if len(description) > 870:
            description = description[:867] + "..."

    except:
        pass
    return photo_link, description


old = []
def run_check():
    global old
    media_group = []
    # Проверка наличия файла (костыль).
    try:
        f = open(keysearch + ".txt", 'r')
    except:
        f = open(keysearch + ".txt", 'x')
        f.close()
    finally:
        f = open(keysearch + ".txt", 'r')
        t = f.read()
    try:
        #for ads in response['ads']:
        #   link = ads['ad_link']
        #    names = ads['subject']
        #    if int(ads['price_byn']) != 0:
        #        price = int(ads['price_byn']) / 100
        #    else:
        #        price = "Договорная"



        r = requests.get(url, params=payload)
        result = r.json()
        for ads in result['ads']:
            link = ads['ad_link']
            names = ads['subject']
            if int(ads['price_usd']) != 0:
                price = int(ads['price_usd']) / 100
            else:
                price = "Договорная"
        #print(result)
        #ids = [ads["ad_id"] for ads in result['ads']]
        #if ids != old:
            bot.send_message(user_id, f'Объявление: {names}, Цена: ${price} , {link}')
        #old = ids
    except Exception as e:
        bot.send_message(user_id, e)
    threading.Timer(60.0, run_check).start()

print("run threading")
run_check()
print("pooling")
while True:
    try:
        #print("start")
        bot.polling(none_stop=True, interval=5)
    except:
        pass