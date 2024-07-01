- [Daily Exchange Rate bemutatása](#daily-exchange-rate-bemutatása)
  - [Leírás](#leírás)
  - [Fő Funkcionalitás](#fő-funkcionalitás)
  - [Futtatási Feltételek](#futtatási-feltételek)
  - [Használat](#használat)
    - [Példa használatára](#példa-használatára)

# Daily Exchange Rate bemutatása

## Leírás

Egy olyan eszköz, amely az MNB (Magyar Nemzeti Bank) hivatalos oldaláról letölti a napi árfolyamokat, majd ezek alapján megadott dátum és valuta alapján kiszámítja, hogy az adott valuta hány forintot ér.

## Fő Funkcionalitás

- Árfolyamok letöltése: A program automatikusan letölti az aktuális napi árfolyamokat az MNB weboldaláról.
- Árfolyamok keresése: A letöltött árfolyamokból a program kikeresi a megadott dátum és valuta alapján az adott valuta forintban kifejezett értékét.

## Futtatási Feltételek

A program futtatásához Python interpreter, Python Venv, illetve Bash szükséges.

```sh
sudo apt install -y python3
sudo apt install -y python3-venv
```

Add meg a szkriptnek a megfelelő jogosultságokat, illetve a terminálon belül menj bele a letöltött mappába.

```sh
cd <projekt_mappa_eleresi_ut>
chmod 777 exchange
```

## Használat

A program a következő argumentumokat fogadja:

1. **Valuta**: Az átváltandó valuta kódja (pl. USD, EUR, stb.).
2. **Dátum**: (opcionális) Az árfolyam lekérdezésének dátuma (pl. 2021-05-04, 2021.05.04, 2021/05/04 stb.).
3. **Fájlnév**: (opcionális) A fájlok elérési útvonala, melyek tartalmazzák a keresendő dátumokat.

### Példa használatára

```sh
./exchange USD 2021-05-04 2024.02.04
```

```sh
./exchange EUR file1.txt file2.txt
```

```sh
./exchange USD file1.txt 2021.05.04 file2.txt 2024.02.04
```