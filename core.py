# __author__ = 'Yudin'

import json
import requests
import enum
import time
import re

# Временные данные
userId = '76561198122735294'


class GameOptions(enum.Enum):
    Dota2 = '570'
    CS = '730'
    TF2 = '440'


class SteamUrl:
    COMMUNITY_URL = "http://steamcommunity.com/"


def get_user_inventory(user_id):
    inventory = requests.get(SteamUrl.COMMUNITY_URL + 'inventory/' + user_id + '/730/2?l=english&count=5000').json()
    item_quanity = len(inventory['descriptions'])
    i = 0
    inventory_items = []
    while i <= item_quanity - 1:
        inventory_item = inventory['descriptions'][i]['market_hash_name']
        inventory_items.append(inventory_item)
        i = i + 1

    return inventory_items


def fetch_price(inventory_items):
        item_quanity = len(inventory_items)
        i = 0
        amounth = 0.00
        while i <= item_quanity - 1:
            item = inventory_items[i]
            response = requests.get(SteamUrl.COMMUNITY_URL + 'market/priceoverview/?currency=1&appid=730&market_hash_name='
                            + item).json()
            price = re.sub("[^0-9.]", "", response['lowest_price'])

            price_float = float(price)
            amounth = amounth + price_float
            i = i + 1
            time.sleep(3)

        return "%.2f" % amounth

print(get_user_inventory(userId))
