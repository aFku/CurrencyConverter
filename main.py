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
    _base = None
    _relative = None

    def __init__(self, url, params):
        super().__init__(url, params)

    def getapikey(self):
        return self.__API.getkey()

    def getbasecurrency(self):
        return self._base

    def getrelativecurrencys(self):
        return self._relative

    def getdatejson(self):
        return super().getrequestobj().json()

    def getratio(self, currency: str):
        currency = currency.upper()
        if currency in [up.upper() for up in self._relative]:
            try:
                return self.getdatejson()["quotes"][self._base + currency]
            except KeyError:
                raise ValueError("No " + currency + " in currency database!")
        else:
            raise ValueError("No " + currency + " in currency database!")


class CurrencyLive(CurrencyConnection):

    def __init__(self, base: str, relative: list):
        self._base = base
        self._relative = relative
        params = {'access_key': super().getapikey(),
                  'currencies': super().getbasecurrency() + "," + ",".join(super().getrelativecurrencys()),
                  'format': 1}
        super().__init__('http://apilayer.net/api/live',  params)


class CurrencyHistorical(CurrencyConnection):

    def __init__(self, base: str, relative: list, date: datetime.date):
        self._base = base
        self._relative = relative
        params = {'access_key': super().getapikey(),
                  'currencies': super().getbasecurrency() + "," + ",".join(super().getrelativecurrencys()),
                  'date': str(date),
                  'format': 1}
        super().__init__('http://apilayer.net/api/historical',  params)


class CurrencyTimeAnalyze:

    @staticmethod
    def getperiodratio(base: str, relative: list, start_date: datetime.date, end_date: datetime.date):
        date = start_date
        result = dict([(curr, []) for curr in relative])
        while date != end_date:
            tmpCurrency = CurrencyHistorical(base, relative, date)
            for curr in relative:
                result[curr].append((tmpCurrency.getratio(curr), str(date)))
            date += datetime.timedelta(days=1)
        for key in result.keys():
            result[key] = tuple(result[key])
        return result



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
    relative = ["PLN", "GBP", "USD"]
    xd = CurrencyTimeAnalyze.getperiodratio("USD", relative, datetime.datetime.now().date() - datetime.timedelta(days=10),
                                            datetime.datetime.now().date() - datetime.timedelta(days=1))
    print(xd)
    print(datetime.datetime.now().date() - datetime.timedelta(days=1))
if __name__ == "__main__":
    main()

