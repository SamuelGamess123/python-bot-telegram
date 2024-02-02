import telebot
import requests
import os
import time
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Defina o token do seu bot do Telegram
TOKEN = os.getenv('TOKEN')

# Cria uma instância do bot
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
@app.route("/", methods=['POST'])
    def index():
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook()
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Olá! Envie um link de um arquivo HTML e eu vou enviá-lo de volta.')

# Função para lidar com mensagens de texto recebidas
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    text = message.text
    if text.startswith('http'):
        file_url = text
        response = requests.get(file_url)
        if response.status_code == 200:
            with open("download.html", 'wb') as file:
                file.write(response.content)
            with open("download.html", 'rb') as file:
                bot.send_document(message.chat.id, file)
            os.remove("download.html")
        else:
            bot.reply_to(message, f'Falha ao baixar o arquivo HTML, seu código de retorno é: {response.status_code}')
    else:
        bot.reply_to(message, 'Por favor, envie um link válido para um arquivo HTML.')
