from sys import argv
from datetime import datetime
from mnb_parser import getExchangeRate
from mnb_handler import getExcel

def main():
    currency = argv[1]

    def processData(text: str) -> str:
        date = datetime.strptime(text, "%Y.%m.%d")
        return str(getExchangeRate(getExcel(date.year), date, currency))

    for arg in argv[2:]:
        if len(arg.split(".")) == 3:
            print(processData(arg))
        else:
            with open(arg, "r") as f:
                result = map(processData, [line.strip() for line in f])
                print('\n'.join(result))

if __name__ == "__main__":
    main()
