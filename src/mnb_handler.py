from pandas import read_excel, DataFrame
from urllib.request import urlretrieve
from os import makedirs
from os.path import exists
from shutil import rmtree

from classes import mnbConsts


def downloadExcel(year: int = None, deletePreviousFiles = False):
    if deletePreviousFiles and exists(mnbConsts.excelFolderPath):
        rmtree(mnbConsts.excelFolderPath)
    
    if not exists(mnbConsts.excelFolderPath):
        makedirs(mnbConsts.excelFolderPath)

    urlretrieve(mnbConsts.getUrl(year), mnbConsts.getExcelPath(year))


def getExcel(year: int = None) -> DataFrame:
    if not exists(mnbConsts.getExcelPath(year)):
        downloadExcel(year)

    return read_excel(mnbConsts.getExcelPath(year))
