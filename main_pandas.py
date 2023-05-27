import pandas as pd

PRODIO_IMPORT_HEADERS = ['Klient;\
                         Oczekiwany termin realizacji;\
                         Termin potwierdzony;\
                         Zewn. nr zamówienia;\
                         Produkt;\
                         Sztuk;\
                         Uwagi dla wszystkich;\
                         Uwagi niewidoczne dla produkcji;\
                         Atrybut 1 (opcjonalnie);\
                         Atrybut 2 (opcjonalnie);\
                         Atrybut 3 (opcjonalnie)']

# path to BOM.xls file
xls_bom = "/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xls"

# convert .xls file to .csv
read_file = pd.read_excel(xls_bom, sheet_name="Całość")
read_file.to_csv(r"bom_temp.csv", index=None, header=True)

# convert .csv to pandas DataFrame
bom_csv = pd.read_csv("bom_temp.csv", skiprows=12)


print(bom_csv.iloc[0])