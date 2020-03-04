import requests
import datetime
import json


class API:

    __API_KEY = None

    def __init__(self, key):
        self.__API_KEY = key

    def getkey(self):
        return self.__API_KEY


class Connection:
    __url = None
    __params = {}
    __request = None
    __last_update = None

    def __init__(self, url, params: dict):
        self.__url = url
        self.__params = params
        self.update_request()

    def update_request(self):
        self.__request = requests.get(self.__url, params=self.__params)
        self.__last_update = datetime.datetime.now()

    def getrequest_json(self):
        return self.__request.json()

    def getupdate_date(self):
        return self.__last_update


class JSONManager:
    __jsondata = None

    def __init__(self, data : dict):
        self.__jsondata = json.dumps(data)

    def save_data_tofile(self):
        pass
