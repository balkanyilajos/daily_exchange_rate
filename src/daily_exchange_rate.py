from sys import argv
from datetime import datetime
from mnb_parser import getExchangeRate
from mnb_handler import getExcel

def main():
    currency = argv[1]

    if len(argv[2].split(".")) == 3:
        for value in argv[2:]:
            date = datetime.strptime(value, "%Y.%m.%d")
            print(getExchangeRate(getExcel(date.year), date, currency))
   

if __name__ == "__main__":
    main()
