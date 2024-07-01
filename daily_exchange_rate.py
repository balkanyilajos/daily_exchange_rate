from sys import argv
from datetime import datetime
from pandas import read_excel, DataFrame
from re import match, findall
from urllib.request import urlretrieve
from os import makedirs
from os.path import exists
from shutil import rmtree

class mnb_consts:
    date_row = "Dátum/ISO"
    unit_row = "Egység"

    excel_folder_path = "./files"

    def get_url(year: int = None) -> str:
        src = "https://www.mnb.hu/arfolyam-letoltes"
        return f"{src}/?year={year}" if year else src
    
    def get_excel_path(year: int = None) -> str:
        if year:
            return f"{mnb_consts.excel_folder_path}/{year}.xlsx"
        else:
            return f"{mnb_consts.excel_folder_path}/all.xlsx"

def download_excel(year: int = None, delete_previous_files = False):
    if delete_previous_files and exists(mnb_consts.excel_folder_path):
        rmtree(mnb_consts.excel_folder_path)
    
    if not exists(mnb_consts.excel_folder_path):
        makedirs(mnb_consts.excel_folder_path)

    if not exists(mnb_consts.get_excel_path(year)):
        urlretrieve(mnb_consts.get_url(year), mnb_consts.get_excel_path(year))

def get_excel(year: int = None) -> DataFrame:
    download_excel(year)
    return read_excel(mnb_consts.get_excel_path(year))

def get_exchange_rate(excel: DataFrame, date: datetime, currency: str) -> float:
    unit_row = excel[excel[mnb_consts.date_row] == mnb_consts.unit_row]
    date_row = excel[excel[mnb_consts.date_row] == date]

    exchange_rate = float(date_row[currency].values[0])
    unit = float(unit_row[currency].values[0])

    return exchange_rate * unit

def str_to_date(date: str, year_position=1, month_position=2, day_position=3) -> datetime | None:
    regex_date = match(pattern=r"^(\d+).(\d+).(\d+)$", string=date)

    if regex_date is None:
        return None

    year = int(regex_date.group(year_position))
    month = int(regex_date.group(month_position))
    day = int(regex_date.group(day_position))

    return datetime(year, month, day)

def main():
    currency = argv[1]

    def process_data(date: datetime) -> float:
        return get_exchange_rate(get_excel(date.year), date, currency)

    for arg in argv[2:]:
        if date := str_to_date(arg):
            print(process_data(date))
            continue

        assert exists(arg), f"ERROR: '{arg}' not an existing file or date input!"

        with open(arg, "r") as f:
            dates_generator = (date for line in f
                                        for date in findall(r"\d+.\d+.\d+", line))
            
            for date in dates_generator:
                print(process_data(str_to_date(date)))

if __name__ == "__main__":
    main()
