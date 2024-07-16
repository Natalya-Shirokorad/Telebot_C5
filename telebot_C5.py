import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, APIExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = (f'Доброго времени суток, уважаемый(ая) {message.chat.username}. '
            f'Чтобы начать работу, введите команду боту следующим образом:\n'
            f'имя валюты в какую валюту перевести количество переводимой валюты\n'
            f'Для просмотра доступных валют введите команду /values')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        if len(values) != 3:
            raise APIExeption("Cлишком много параметров.")

        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}.')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


