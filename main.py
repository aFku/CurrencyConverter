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

    def update_param(self, key, value):
        self.__params[key] = value


class JSONManager:
    __jsondata = None
    __filename = None

    def __init__(self, data: dict, filename: str):
        self.__jsondata = json.dumps(data)
        self.__filename = filename

    def save_data_tofile(self):
        with open(self.__filename, "w") as jsonfile:
            jsonfile.writelines(self.__jsondata)

    def update_data(self, data: dict):
        self.__jsondata = data


def main():
    currency_api = API('2639ccac02d7c15359d45f9a2bc9d8ea')
    currency_connection = Connection('http://apilayer.net/api/live', {'access_key': currency_api.getkey(),
                                                                      'currencies': 'USD,EUR,CNY,HKD',
                                                                      'format': 1})
    currency_filemanager = JSONManager(currency_connection.getrequest_json(), "currency.json")
    currency_filemanager.save_data_tofile()


if __name__ == "__main__":
    main()

