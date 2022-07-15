import requests
import json
from conf import keys


class ConvertionException(Exception):
    pass

class Convertor:
    @staticmethod
    def convert(quote, base, amount):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {quote}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)
        if int(amount) % 10 == 1:
            text = f'Цена {amount} {quote}а в {base}ах - {total_base}'
        else:
            text = f'Цена {amount} {quote}ов в {base}ах - {total_base}'
        return text