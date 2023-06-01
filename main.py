import pandas as pd
from validators import ProductValidator

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


# path to BOM.xls file
xls_bom = input("Podaj pelna nazwe pliku arkusza BOM (wraz z rozszerzeniem .xls lub .xlsx):\n")

# convert .xls file to .csv
read_file = pd.read_excel(xls_bom, sheet_name="Całość")
read_file.to_csv(r"bom_temp.csv", index=None, header=True)

# convert .csv to pandas DataFrame
bom_csv = pd.read_csv("bom_temp.csv", skiprows=12)

# init of empty DataFrame object to be filled with lines to export to Prodio
prodio_df = pd.DataFrame(columns=PRODIO_IMPORT_HEADERS)
prepare_materials_df = pd.DataFrame(columns=PRODIO_IMPORT_HEADERS)

# pass values identical for every row
client_name = input("Podaj numer klienta zamowienia:\n")
finish_date = input("Podaj oczekiwany termin realizacji obrobki (DD.MM.RRRR):\n")
finish_preparation_date = input("Podaj oczekiwany termin realizacji przygotowania materialu (DD.MM.RRRR):\n")
ext_order_number = input("Podaj wewnetrzny numer zamowienia (format DD.MM.RRRR_[inicjaly]_[liczba porzadkowa]):\n")

# iteration through whole bom_csv file/DataFrame to pick data from it and swap to prodio csv
for i in range(len(bom_csv)):
    # read single line with i index
    line = bom_csv.loc[i]
    # read data needed for product validation
    product_name = str(line["Nazwa"])
    material = line["Gatunek"]
    x_dim = line["Wymiar"]

    # create ProductValidator object
    validator = ProductValidator(product_name=product_name,
                                 material=material,
                                 x_dimension=x_dim)
    # validation check and var assignment of validation result
    is_product, plate_destined_for, cylindrical_procedure = validator.validate_all()

    if not is_product or plate_destined_for == "omit":
        continue
    else:
        if (plate_destined_for == "prepare" and cylindrical_procedure != "ready") or (cylindrical_procedure == "prepare"):
            # concatenate data needed for field "Uwagi dla wszystkich"
            dimensions = "".join([str(s) for s in line[3:8]])
            remarks_for_everyone = material + " " + dimensions + " " + product_name

            # create pandas Series line for material preparation 
            prepare_material_prodio_line = pd.Series(index=PRODIO_IMPORT_HEADERS)
            prepare_material_prodio_line["Klient"] = client_name
            prepare_material_prodio_line["Oczekiwany termin realizacji"] = finish_preparation_date
            prepare_material_prodio_line["Zewn. nr zamówienia"] = ext_order_number + "P"
            prepare_material_prodio_line["Produkt"] = "PRZYGOTOWANIE MATERIAŁU"
            prepare_material_prodio_line["Sztuk"] = line["Ilość"]
            prepare_material_prodio_line["Uwagi dla wszystkich"] = remarks_for_everyone
            prepare_material_prodio_line["Uwagi niewidoczne dla produkcji"] = ""
            prepare_materials_df.loc[len(prepare_materials_df)] = prepare_material_prodio_line
        else:
            prodio_line = pd.Series(index=PRODIO_IMPORT_HEADERS)
            prodio_line["Klient"] = client_name
            prodio_line["Oczekiwany termin realizacji"] = finish_date
            prodio_line["Zewn. nr zamówienia"] = ext_order_number
            prodio_line["Produkt"] = product_name
            prodio_line["Sztuk"] = line["Ilość"]
            prodio_line["Uwagi dla wszystkich"] = "A1"
            prodio_line["Uwagi niewidoczne dla produkcji"] = material + "; PILNE"
            prodio_df.loc[len(prodio_df)] = prodio_line

merged_df = pd.concat([prodio_df, prepare_materials_df], ignore_index=True, sort=False)
merged_df.to_csv('generated_prodio_import.csv', sep=";", index=False)