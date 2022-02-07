import telebot

token = '_5240966312:AAGpfBqxEiHgAmIA_8LJBHO3-8tRfHsLU3w'

bot = telebot.TeleBot(token)

name = 'zz'

@bot.message_handler(content_types=["text"])
def echo(message):
    if name in message.text:
        text = 'Ба! Знакомые все лица'
    else:
        text = message.text
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)