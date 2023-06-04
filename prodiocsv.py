import pandas as pd
import os
from validators import ProductValidator

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


def convert_xls_to_dataframe(file) -> pd.read_excel():
    return pd.read_excel(file, sheet_name="Całość", skiprows=12, keep_default_na=False)


def get_client_name(path: str) -> str:
     filename = os.path.split(path)
     return filename[1].split("_")[0]


def validate_bom_line(product:Product) -> ProductValidator.validate_all():
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
                         client_name,
                         ext_order_number,
                         prepare_finish_date,
                         finish_date,
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


if __name__ == "__main__":
    pass