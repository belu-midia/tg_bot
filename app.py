# belu midia, pj-02, intpy-2
import telebot
from config import  TOKEN, keys
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    text = '''Чтобы начать работу введите запрос боту в следующем формате:
<название валюты><в какую валюту перевести><количество переводимой валюты>
Увидеть список всех доступных валют: /values'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def  convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Неверно введён запрос:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
