import pandas as pd
from validators import validate_product_name

PRODIO_IMPORT_HEADERS = ['Klient',\
                         'Oczekiwany termin realizacji',\
                         'Termin potwierdzony',\
                         'Zewn. nr zamówienia',\
                         'Produkt',\
                         'Sztuk',\
                         'Uwagi dla wszystkich',\
                         'Uwagi niewidoczne dla produkcji',\
                         'Atrybut 1 (opcjonalnie)',\
                         'Atrybut 2 (opcjonalnie)',\
                         'Atrybut 3 (opcjonalnie)']

PRODIO_EXAMPLE_ROW = ['NABR008',\
                      '2023.05.30',
                      '',
                      '2023.05.27_GL_1',
                      '22_018A_T_10_1_023',
                      '3',
                      'A3',
                      'HOLDAX; PILNE',
                      '',
                      '',
                      ''
]


# path to BOM.xls file
xls_bom = "/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xls"

# convert .xls file to .csv
read_file = pd.read_excel(xls_bom, sheet_name="Całość")
read_file.to_csv(r"bom_temp.csv", index=None, header=True)

# convert .csv to pandas DataFrame
bom_csv = pd.read_csv("bom_temp.csv", skiprows=12)

# init of empty DataFrame object to be filled with lines to export to Prodio
prodio_df = pd.DataFrame(columns=PRODIO_IMPORT_HEADERS)

# iteration through whole bom_csv file/DataFrame to pick data from it and swap to prodio csv
for i in range(len(bom_csv)):
    line = bom_csv.loc[i]
    product_name = str(line["Nazwa"])
    prodio_line = pd.Series(index=PRODIO_IMPORT_HEADERS)
    prodio_line["Klient"] = "NATS012"
    prodio_line["Oczekiwany termin realizacji"] = "2023.05.30"
    prodio_line["Zewn. nr zamówienia"] = "2023.05.27_GL_1"
    prodio_line["Produkt"] = product_name
    prodio_line["Sztuk"] = line["Ilość"]
    prodio_line["Uwagi dla wszystkich"] = "A1"
    prodio_line["Uwagi niewidoczne dla produkcji"] = line["Gatunek"] + "; PILNE"
    prodio_df.loc[len(prodio_df)] = prodio_line

prodio_df.to_csv('generated_prodio_import.csv', sep=";")