import requests
import json
from config import keys, headers, payload


class ConversionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}.')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=" \
              f"{base_ticker}&from={quote_ticker}&amount={amount}"
        response = requests.request("GET", url, headers=headers, data=payload)
        total_base = json.loads(response.content)['result']

        return total_base
