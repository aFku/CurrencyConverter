import requests
import datetime
import json
import matplotlib.pyplot as plt



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

    # Change to time frame queries https://currencylayer.com/documentation

    __result = {}
    __base = None
    __relative = None
    __start_date = None
    __end_date = None

    def __init__(self, base: str, relative: list, start_date: datetime.date, end_date: datetime.date):
        self.__base = base
        self.__relative = relative
        self.__start_date = start_date
        self.__end_date = end_date

        date = start_date
        self.__result = dict([(curr, []) for curr in relative])
        while date != end_date:
            tmpCurrency = CurrencyHistorical(base, relative, date)
            for curr in relative:
                self.__result[curr].append((tmpCurrency.getratio(curr), str(date)))
            date += datetime.timedelta(days=1)
        for key in self.__result.keys():
            self.__result[key] = tuple(self.__result[key])

    def drawgraph_periodratio(self, curr: str):
        axis_x = [date[1] for date in self.__result[curr]]
        axis_y = [value[0] for value in self.__result[curr]]
        plt.plot(axis_x, axis_y)
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title("Ratio for " + self.__base + " : " + curr)
        plt.show()


def main():
    relative = ["PLN", "GBP", "USD"]
    xd = CurrencyTimeAnalyze("USD", relative, datetime.datetime.now().date() - datetime.timedelta(days=10),
                                            datetime.datetime.now().date() - datetime.timedelta(days=1))
    xd.drawgraph_periodratio("PLN")
if __name__ == "__main__":
    main()

