import telebot

token = '_5240966312:AAGpfBqxEiHgAmIA_8LJBHO3-8tRfHsLU3w'

bot = telebot.TeleBot(token)
name = "Vasiya"

@bot.message_handler(content_types=["text"])
def echo(message):
    if name in message.text:
        text = 'Ба! Знакомые все лица'
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)