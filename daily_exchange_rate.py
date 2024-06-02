from urllib.request import urlretrieve
from os import makedirs
from os.path import exists
from pathlib import Path
from sys import argv
from shutil import rmtree
from datetime import datetime
from pandas import read_excel, DataFrame

from mnb_handler import getExchangeRate

def downloadFile(url: str, filePath: Path, deletePreviousFiles = False):
    if deletePreviousFiles:
        cleanup(filePath.parent)

    makedirs(filePath.parent)
    urlretrieve(url, filePath)

def findInFile(filePath: Path, date: datetime):
    f: DataFrame = read_excel(filePath)
    getExchangeRate(excel=f, date=date)
    #print(f)

#def writeV

def cleanup(destination: Path):
    if exists(destination):
        rmtree(destination)

def main():
    date: datetime = datetime.strptime(argv[1], "%Y.%m.%d")
    url = f"https://www.mnb.hu/arfolyam-letoltes/?year={date.year}"
    mnbFile = f"{date.year}.xlsx"
    mnbPath = Path("./files").joinpath(mnbFile)

    downloadFile(url, mnbPath, deletePreviousFiles=True)
    findInFile(mnbPath, date)
    #cleanup(filePath.parent)

if __name__ == "__main__":
    main()
