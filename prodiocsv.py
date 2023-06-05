import pandas as pd
import os
from validators import ProductValidator
import datetime as dt
import re

class Product:
    def __init__(self, product_name:str="",
                 material:str="",
                 dimensions:list=[],
                 quantity:list=""):
        self.name = str(product_name)
        self.material = str(material)
        self.dimensions = dimensions
        self.quantity = str(quantity)


    def get_product_data(self, line:pd.Series):
         self.name = line["Nazwa"]
         self.material = line["Gatunek"]
         self.dimensions = line[3:8]
         self.quantity = line["Ilość"]



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


def convert_xls_to_dataframe(file) -> pd.read_excel:
    return pd.read_excel(file, sheet_name="Całość", skiprows=12, keep_default_na=False)


def get_client_name(path: str) -> str:
     filename = os.path.split(path)
     return filename[1].split("_")[0]


def today_date_to_str() -> str:
     now = dt.date.today()
     day = str(now.day) if now.day >= 10 else "0" + str(now.day)
     month = str(now.month) if now.month >= 10 else "0" + str(now.month)
     year = str(now.year)
     return day + "."  + month + "." + year


def is_str_date_later(date_to_check: str, reference_date: str) -> bool:
     if int(date_to_check.split('.')[0]) > int(reference_date.split('.')[0]):
          return True
     else:
          return False


def create_order_id(initials: str) -> str:
    date = today_date_to_str()
    pattern = r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}\_" + str(initials)
    ord_num = ""
    # read log file with order
    try:
        # read all log file lines if file exists
        with open('.ord_nums_log.txt', "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        # create file if it does not exist
        with open('.ord_nums_log.txt', "w") as f:
            pass
    # check whether log file needs clearing and then look for regex matches in existing lines
    for line in lines:
        # check if order numbers in log file are older than today
        # if so - clear the log file and do not check lines pattern
        if is_str_date_later(date, line.split("_")[0]):
             with open('.ord_nums_log.txt', "w") as f:
                pass
             break
        # if log file has order numbers only with today date - check which lines correspond to
        # passed initials
        if re.match(pattern, line):
             ord_num = line[:-1]
    
    # create order number
    if ord_num == "":
         ord_num = date + "_" + initials + "_1"
    else:
         ord_num = ord_num[:-1] + str(int(ord_num[-1]) + 1 )

    # write order number into log file
    with open('.ord_nums_log.txt', "a") as f:
        f.write(ord_num + "\n")
    return ord_num


def validate_bom_line(product:Product) -> ProductValidator.validate_all:
    # read data needed for product validation
    product_name = product.name
    material = str(product.material)
    x_dim = str(product.dimensions[0])

    # create ProductValidator object
    validator = ProductValidator(product_name=product_name,
                                 material=material,
                                 x_dimension=x_dim)
    # validation check and var assignment of validation result
    validators = validator.validate_all()
    return validators


def concat_data_for_preparation(product:Product) -> str:
    # concatenate data needed for field "Uwagi dla wszystkich"
    dimensions = "".join([str(s) for s in product.dimensions])
    return product.material + " " + dimensions + " " + product.name


def write_validated_line(product:Product,
                         validators:tuple,
                         prepare_dataframe:pd.DataFrame,
                         machine_dataframe:pd.DataFrame,
                         client_name: str,
                         ext_order_number: str,
                         prepare_finish_date: str,
                         finish_date: str,
                         is_urgent=True):
    
    is_product, plate_destined_for, cylindrical_procedure = validators
    
    if not is_product or plate_destined_for == "omit":
            return None
    else:
        if (plate_destined_for == "prepare" and cylindrical_procedure != "ready") or (cylindrical_procedure == "prepare"):
            remarks_for_everyone = concat_data_for_preparation(product)
            # create pandas Series line for material preparation 
            prepare_material_prodio_line = pd.Series(index=PRODIO_IMPORT_HEADERS)
            prepare_material_prodio_line["Klient"] = client_name
            prepare_material_prodio_line["Oczekiwany termin realizacji"] = prepare_finish_date
            prepare_material_prodio_line["Zewn. nr zamówienia"] = ext_order_number + "P"
            prepare_material_prodio_line["Produkt"] = "PRZYGOTOWANIE MATERIAŁU"
            prepare_material_prodio_line["Sztuk"] = product.quantity
            prepare_material_prodio_line["Uwagi dla wszystkich"] = remarks_for_everyone
            prepare_material_prodio_line["Uwagi niewidoczne dla produkcji"] = ""
            # insert pandas Series created above into dataframe
            prepare_dataframe.loc[len(prepare_dataframe)] = prepare_material_prodio_line

        # create pandas Series line for product machining
        prodio_line = pd.Series(index=PRODIO_IMPORT_HEADERS)
        prodio_line["Klient"] = client_name
        prodio_line["Oczekiwany termin realizacji"] = finish_date
        prodio_line["Zewn. nr zamówienia"] = ext_order_number
        prodio_line["Produkt"] = product.name
        prodio_line["Sztuk"] = product.quantity
        prodio_line["Uwagi dla wszystkich"] = "A1"
        prodio_line["Uwagi niewidoczne dla produkcji"] = product.material + "; PILNE" if is_urgent else product.material
        # insert pandas Series created above into dataframe
        machine_dataframe.loc[len(machine_dataframe)] = prodio_line
