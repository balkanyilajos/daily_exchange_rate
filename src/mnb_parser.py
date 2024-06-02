from pandas import DataFrame
from datetime import datetime

from classes import mnbConsts

def getExchangeRate(excel: DataFrame, date: datetime, currency: str) -> int:
    for index, value in enumerate(excel[mnbConsts.dateRow]):
        if value == date:
            return excel[currency][index]

