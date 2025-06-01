import requests 
from bs4 import BeautifulSoup
import telebot
import re

bot = telebot.TeleBot('token')

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "кидай ссылку пинтерест")



@bot.message_handler(content_types=['text'])
def sa(message):
    # Use regex to find the URL in the message text
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, message.text)

    if urls:
        url = urls[0]  # Get the first URL found
        if 'https://ru.pinterest.com/pin/' in url or 'https://pin.it/' in url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                video = soup.find("video")
                if video:
                    a = video["src"]
                    convert_url = a.replace("hls", "720p").replace("m3u8", "mp4")
                    bot.send_message(message.chat.id, convert_url)
                else:
                    img = soup.find("img")
                    if img:
                        bot.send_message(message.chat.id, img["src"])
                    else:
                        bot.send_message(message.chat.id, "нету такова")



bot.polling()