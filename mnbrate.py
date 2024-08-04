from sys import argv
from datetime import datetime
from pandas import read_excel, DataFrame
from re import match, findall
from urllib.request import urlretrieve
from os import makedirs
from os.path import exists
from shutil import rmtree

from typing import Union, List, Generator

_date_row = "Dátum/ISO"
_unit_row = "Egység"

def get_excel_path(excel_folder_path: str, year: int = None) -> str:
    ''' 
    Return:
        - Excel file path
    
    The function doesn't guarantee that the file exists. 
    '''
    if year:
        return f"{excel_folder_path}/{year}.xlsx"
    else:
        return f"{excel_folder_path}/all.xlsx"

def get_excel_url(year: int = None) -> str:
    '''
    Return:
        - Excel URL from MNB
    '''
    src = "https://www.mnb.hu/arfolyam-letoltes"
    return f"{src}/?year={year}" if year else src

def download_excel(excel_folder_path: str, year: int = None, delete_previous_files = False):
    '''
    It downloads Excel file to excel_folder_path. Year variable is used for define the filename.
    '''
    if delete_previous_files and exists(excel_folder_path):
        rmtree(excel_folder_path)
    
    makedirs(excel_folder_path, exist_ok=True)
    if not exists(get_excel_path(excel_folder_path, year)):
        urlretrieve(get_excel_url(year), get_excel_path(excel_folder_path, year))

def get_excel(excel_folder_path: str, year: int = None) -> DataFrame:
    '''
    Return:
        - Excel file content
    It downloads the excel file from the MNB's official website.
    '''
    download_excel(excel_folder_path, year)
    return read_excel(get_excel_path(excel_folder_path, year))

def get_exchange_rate(excel: DataFrame, date: datetime, currency: str) -> float:
    '''
    Return:
        - Exchange rate from excel
    '''
    unit_row = excel[excel[_date_row] == _unit_row]
    date_row = excel[excel[_date_row] == date]

    assert not date_row.empty, f"ERROR: Date not found [{date.strftime('%Y-%m-%d')}]!"
    assert currency in unit_row, f"ERROR: No currency information [{currency}]!"

    exchange_rate = float(date_row[currency].values[0])
    unit = float(unit_row[currency].values[0])

    return exchange_rate * unit

def date_generator(*args: List[Union[str, datetime]]) -> Generator[datetime, None, None]:
    '''
    Generates date from files and strings.
    Return:
        - date
    '''
    for arg in args:
        if date := _str_to_date(arg):
            yield date
            continue

        assert exists(arg), f"ERROR: '{arg}' not an existing file or date input!"    
        
        with open(arg, "r") as f:
            yield from (_str_to_date(date) for line in f for date in findall(r"\d+.\d+.\d+", line))

def _str_to_date(date: str, year_position=1, month_position=2, day_position=3) -> datetime | None:
    regex_date = match(pattern=r"^(\d+).(\d+).(\d+)$", string=date)

    if regex_date is None:
        return None

    year = int(regex_date.group(year_position))
    month = int(regex_date.group(month_position))
    day = int(regex_date.group(day_position))

    return datetime(year, month, day)

def cleanup(excel_folder_path):
    rmtree(excel_folder_path)

# Error handling
def _usage_message() -> str:
    return f"Usage: {argv[0]} <currency> [<file_or_date> ...]"

def _help_message() -> str:
    return (
        _usage_message() +
        "\nArguments:"
        "  <currency>           The currency to be converted.",
        "  <file> or <date>     Additional arguments which can be filenames or dates."
        "\nOptions:"
        "  --help               Show this help message and exit."
    )

def _check_argv():
    if "--help" in argv: 
        print(_help_message())
        exit(0)

    assert len(argv) >= 2, f"ERROR: No currency provided.\n{_usage_message()}"
    assert len(argv) >= 3, f"ERROR: No files or dates provided.\n{_usage_message()}"

def main():
    _check_argv()
    currency = argv[1]
    excel_folder_path = "./excel_files"

    for date in date_generator(*argv[2:]):
        print(get_exchange_rate(get_excel(excel_folder_path, date.year), date, currency))

    cleanup(excel_folder_path)

if __name__ == "__main__":
    main()
