# __author__ = 'Yudin'

import json
import requests
import time
import re

# Временные данные
userId = '76561198122735294'
apikey = '1D491D713C988BDD4BB45512E1E929A6'


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

def get_users_inventory(users_id: list):
    user_quanity = len(users_id)
    res = {}
    i = 0
    while i <= user_quanity - 1:
        inventory_value = fetch_price(get_user_inventory(users_id[i]))
        res = {users_id[i], inventory_value}


    return res


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
    return  friendidlist


print(get_users_inventory(get_friends_id_list(userId, apikey)))
