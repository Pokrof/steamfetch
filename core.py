# __author__ = 'Yudin'


import requests
import time
import re


class GameOptions:
    Dota2 = '570'
    CS = '730'
    TF2 = '440'


class Relationship:
    Friend = 'friends'
    All = 'all'


class SteamUrl:
    COMMUNITY_URL = "http://steamcommunity.com/"
    API_URL = "http://api.steampowered.com/"


def get_user_inventory(user_id):
    inventory = requests.get(SteamUrl.COMMUNITY_URL + 'inventory/' + user_id + '/730/2?l=english&count=5000').json()
    item_quanity = len(inventory['descriptions'])
    i = 0
    inventory_items = []
    while i <= item_quanity - 1:
        if inventory['descriptions'][i]['tradable'] == 1:
            inventory_item = inventory['descriptions'][i]['market_hash_name']
            inventory_items.append(inventory_item)
            i = i + 1
        else:
            i = i + 1

    return inventory_items


def fetch_price(inventory_items):
    item_quanity = len(inventory_items)
    i = 0
    amounth = 0.00
    while i <= item_quanity - 1:
        timestart = time.time()
        item = inventory_items[i]
        response = requests.get(SteamUrl.COMMUNITY_URL + 'market/priceoverview/?currency=1&appid=730' +
                                '&market_hash_name=' + item).json()
        price = re.sub("[^0-9.]", "", response['lowest_price'])

        price_float = float(price)
        amounth = amounth + price_float
        i = i + 1
        if time.time()-timestart <= 3:
            time.sleep(3 - (time.time() - timestart))

    return "%.2f" % amounth


def get_friends_list(user_id: str, api_key: str):
    response = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + api_key + '&steamid='
                            + user_id + '&relationship=friend').json()

    return response


def get_friends_id_list(user_id: str, api_key: str):
    friendlist = get_friends_list(user_id, api_key)
    flen = len(friendlist['friendslist']['friends'])

    i = 0
    friendidlist = []
    while i <= flen - 1:
        friendidlist.append(friendlist['friendslist']['friends'][i]['steamid'])
        i = i + 1
    return friendidlist
