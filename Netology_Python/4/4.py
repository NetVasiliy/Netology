import telebot

token = '5240966312:AAGpfBqxEiHgAmIA_8LJBHO3-8tRfHsLU3w'

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)