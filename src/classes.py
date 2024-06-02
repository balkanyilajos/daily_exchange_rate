from pathlib import Path

class mnbConsts:
    dateRow = "Dátum/ISO"
    hufRow = "HUF"
    usdRow = "USD"
    eurRow = "EUR"

    excelFolderPath = "./files"

    def getUrl(year: int = None) -> str:
        src = "https://www.mnb.hu/arfolyam-letoltes"
        return f"{src}/?year={year}" if year else src
    
    def getExcelPath(year: int = None) -> str:
        if year:
            return f"{mnbConsts.excelFolderPath}/{year}.xlsx"
        else:
            return f"{mnbConsts.excelFolderPath}/all.xlsx"
        
