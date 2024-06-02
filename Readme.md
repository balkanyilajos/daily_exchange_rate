# Daily Exchange Rate bemutatása

## Leírás

Egy olyan eszköz, amely az MNB (Magyar Nemzeti Bank) hivatalos oldaláról letölti a napi árfolyamokat, majd ezek alapján megadott dátum és valuta alapján kiszámítja, hogy az adott valuta mennyi forintot ér.

## Fő Funkcionalitás

- Árfolyamok letöltése: A program automatikusan letölti az aktuális napi árfolyamokat az MNB weboldaláról.
- Árfolyamok keresése: A letöltött árfolyamokból a program kikeresi a megadott dátum és valuta alapján az adott valuta forintban kifejezett értékét.

## Használat

A program a következő argumentumokat fogadja:

1. **Valuta**: Az átváltandó valuta kódja (pl. USD, EUR, stb.).
2. **Dátum**: Az árfolyam lekérdezésének dátuma (pl. 2021-05-04).
3. **Fájlnév**: (opcionális) A fájlok neve, amelyek tartalmazzák a keresendő dátumokat.

Példa használatára:

```sql
./run.sh USD 2021.05.04 2024.02.04
```

```sql
./run.sh EUR file1.txt file2.txt
```

```sql
./run.sh USD file1.txt 2021.05.04 file2.txt 2024.02.04
```

## Futtatási Feltételek

A program futtatásához Python, illetve Bash szükséges



