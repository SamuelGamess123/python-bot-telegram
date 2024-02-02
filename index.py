import telebot
import requests
import os

# Defina o token do seu bot do Telegram
TOKEN = '5998033378:AAF7YqOif4jeHZEYtngObD9sX-r6Cs-aCYg'

# Cria uma instância do bot
bot = telebot.TeleBot(TOKEN)

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
            with open(os.path.basename(file_url), 'wb') as file:
                file.write(response.content)
            with open(os.path.basename(file_url), 'rb') as file:
                bot.send_document(message.chat.id, file)
            os.remove(os.path.basename(file_url))
        else:
            bot.reply_to(message, 'Falha ao baixar o arquivo HTML.')
    else:
        bot.reply_to(message, 'Por favor, envie um link válido para um arquivo HTML.')

# Inicia o bot
bot.remove_webhook()
bot.set_webhook(url="https://python-bot-telegram-a9hi2qsj6-samuelgamess123.vercel.app/")
