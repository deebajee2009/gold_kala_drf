import requests


def get_current_gold_price(self):
        # Example function to get the current gold price
        return 10000000  # This could be fetched from an API or database

class PriceFetchService:
    # Api for gold, currencies, cryptocurrencies proces in Toman from http://brsapi.ir
    PRICE_API_URL = 'https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json'

    @staticmethod
    def fetch_price():
        response = requests.get(PriceService.GOLD_CURRENCY_API_URL)
        data = response.json()
        return data
