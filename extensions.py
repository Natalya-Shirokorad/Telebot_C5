import requests
import json
from config import keys, ACCESS_KEY

class APIExeption(Exception):
    pass
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIExeption(f'Не возможно конвертировать одинаковые валюты {base}.')
        quote_ticker, base_ticker = keys[quote.lower()], keys[base.lower()]

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Неудалось обработать. Не правильно задано количество валюты {amount}')
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Неудалось обработать. Не правильно задано количество валюты {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{ACCESS_KEY}/pair/{quote_ticker}/{base_ticker}/{amount}')
        conversion_rate = json.loads(r.content)['conversion_rate']
        total_base = conversion_rate * amount
        return total_base

