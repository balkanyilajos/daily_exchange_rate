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
_excels_path = "./tmp_mnbrate_excel_folder"

def get_excel_path(year: int = None, excels_path: str = None) -> str:
    ''' 
    Parameters
    - excels_path is used to determine path from the root. \n
      If it's None then default value will be _excels_path variable.
    - year is used to determine path from the root and identify small mnb files. \n
      If it's None then the function downloads data for all years. This can result a slow process.
    Return
    - Excel file path
    
    The function doesn't guarantee that the file exists. 
    If excels_path is None, it's default value will be _excels_path variable.
    '''
    if excels_path is None: excels_path = _excels_path
    today = datetime.today().strftime('%Y-%m-%d')

    if year:
        return f"{excels_path}/{year}_{today}.xlsx"
    else:
        return f"{excels_path}/all_{today}.xlsx"

def get_excel_url(year: int = None) -> str:
    '''
    Parameters.
    - year is used to determine path from the root and identify small mnb files. \n
      If it's None then the function downloads data for all years. This can result a slow process.
    Return
    - Excel URL from MNB
    '''
    src = "https://www.mnb.hu/arfolyam-letoltes"
    return f"{src}/?year={year}" if year else src

def download_excel(year: int = None, excels_path: str = None):
    '''
    It downloads Excel file to excels_path.

    Parameters
    - excels_path is used to determine path from the root. \n
      If it's None then default value will be _excels_path variable.
    - year is used to determine path from the root and identify small mnb files. \n
      If it's None then the function downloads data for all years. This can result a slow process.
    '''
    if excels_path is None: excels_path = _excels_path
    
    makedirs(excels_path, exist_ok=True)
    if not exists(get_excel_path(excels_path=excels_path, year=year)):
        urlretrieve(get_excel_url(year), get_excel_path(excels_path=excels_path, year=year))

def get_excel(year: int = None, excels_path: str = None) -> DataFrame:
    '''
    Parameters
    - excels_path is used to determine path from the root. \n
      If it's None then default value will be _excels_path variable.
    - year is used to determine path from the root and identify small mnb files. \n
      If it's None then the function downloads data for all years. This can result a slow process.
    
    Return
    - Excel file content\n

    It downloads the excel file from the MNB's official website.
    '''
    download_excel(year=year, excels_path=excels_path)
    return read_excel(get_excel_path(year=year, excels_path=excels_path))

def get_exchange_rate(date: datetime, currency: str, excel: DataFrame = None) -> float:
    '''
    Return
    - Exchange rate from excel
    '''
    if excel is None: excel = get_excel(year=date.year)

    unit_row = excel[excel[_date_row] == _unit_row]
    date_row = excel[excel[_date_row] == date]

    assert not date_row.empty, f"ERROR: Date not found [{date.strftime(r'%Y-%m-%d')}]!"
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

def cleanup():
    rmtree(_excels_path)

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

    for date in date_generator(*argv[2:]):
        print(get_exchange_rate(date, currency))

    cleanup()

if __name__ == "__main__":
    main()
