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
    __request = None
    __params = None

    def __init__(self, url: str, params: dict):
        self.__url = url
        self.__params = params
        self.__request = requests.get(url, params)

    def getrequestobj(self):
        return self.__request

    def geturl(self):
        return self.__url

    def getparams(self):
        return self.__params


class CurrencyConnection(Connection):

    __API = API('2639ccac02d7c15359d45f9a2bc9d8ea')
    __base = None
    __relative = None
    __date = None

    def __init__(self, base_curr: str, relative_currs: list, day: int, month: int, year: int):
        self.__base = base_curr.upper()
        self.__relative = relative_currs
        self.__date = str(year) + "-" + str(month) + "-" + str(day)
        super().__init__('http://apilayer.net/api/live', {'access_key': self.__API.getkey(),
                                                          'currencies': self.__base + "," + ",".join(self.__relative),
                                                          'date': self.__date,
                                                          'format': 1})

    def getapikey(self):
        return self.__API.getkey()

    def getbasecurrency(self):
        return self.__base

    def getrelativecurrencys(self):
        return self.__relative

    def getdate(self):
        return self.__date

    def getdatejson(self):
        return super().getrequestobj().json()

    def getratio(self, currency: str):
        currency = currency.upper()
        if currency in [up.upper() for up in self.__relative]:
            try:
                return self.getdatejson()["quotes"][self.__base + currency]
            except KeyError:
                raise ValueError("No " + currency + " in currency database!")
        else:
            raise ValueError("No " + currency + " in currency database!")


class CurrencyTimeAnalyze:

    def getperiodratio(self, currency, first_d: int, first_m: int, first):
        pass



"""
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
"""



def main():
    #USDtoEURGBPPLN = CurrencyConnection("usd", ["pln"], 7, 3, 2020)
    #print(USDtoEURGBPPLN.getratio("PLN"))
    USDtoPLN = Connection('http://apilayer.net/api/historical', {'access_key': '2639ccac02d7c15359d45f9a2bc9d8ea',
                                                          'currencies': 'USD,PLN',
                                                          'date': '2020-03-07',
                                                          'format': 1})
    print(USDtoPLN.getrequestobj().json())
    print(type(str(datetime.datetime.now().date() - datetime.timedelta(days=100))))
if __name__ == "__main__":
    main()

