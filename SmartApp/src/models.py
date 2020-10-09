from enum import Enum
from pydantic import BaseModel



class MyException(Exception):
    pass


class Company:
    def __init__(self, symbol):
        self.name = None
        self.symbol = symbol
        self.sector = None
        self.industry = None


class Index(str, Enum):
    FTSE100 = "FTSE 100"
    SNP500 = "S&amp;P 500"
    DOWJONE = "Dow Jones"


class Configuration(BaseModel):
    index: str = None

    index_map = {
        Index.FTSE100: 'https://en.wikipedia.org/wiki/FTSE_100_Index',
        Index.SNP500: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    }

    def get_url(self):
        return self.index_map[self.index]
