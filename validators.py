import re

VALID_PRODUCT_NAME = "23_002A_T_20_0_2_009"
INVALID_PRODUCT_NAME = "M50-100-A-YW"


def validate_product_name(product_name: str) -> bool:
    pattern = r"^[0-9]{2}_[0-9]{3}"
    return bool(re.match(pattern, product_name))


def validate_material(material: str) -> str:
    MATERIALS_TO_ORDER = ["NC11LV",
                          "SLEIPNER",
                          "HOLDAX",
                          "VANADIS 4E"]
    
    MATERIALS_TO_PREPARE = ["S355",
                            "S235",
                            "C45"]
    
    if material in MATERIALS_TO_ORDER:
        return "order"
    elif material in MATERIALS_TO_PREPARE:
        return "prepare"
    

