import telebot
from conf import TOKEN, keys
from utils import *
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>' \
           '\nУвидеть доступ всех возможных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')
        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        answer = Convertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message,f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message,answer)

bot.polling()