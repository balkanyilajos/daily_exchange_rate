from datetime import datetime
from pandas import read_excel, DataFrame

def getExcel(filePath: str) -> DataFrame:
    return read_excel(filePath)

def getExchangeRate(excel: DataFrame, date: datetime, currency: str = None) -> list[int] | int:
    dateRowName: str = "Dátum/ISO"
    print(excel[dateRowName])
    #excel.loc(excel.iloc[dateRowIndex] == )