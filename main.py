import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException

'''

ВНИМАНИЕ!!!

По соображениям безопасности я свой токен для бота оставлять не буду =)
Перед использованием вставьте свой TOKEN телеграм-бота в файл config.py

'''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте! Чтобы начать работу, введите команду боту в следующем формате в любом регистре: \n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Должно быть ровно 3 параметра!')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'location'])
def unclear(message: telebot.types.Message):
    bot.reply_to(message, 'Я не умею распознавать такой тип данных')


@bot.message_handler(content_types=['voice'])
def soon(message: telebot.types.Message):
    bot.reply_to(message, 'Когда-нибудь здесь появится распознавание голоса...')


bot.polling()
