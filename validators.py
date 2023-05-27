import re

VALID_PRODUCT_NAME = "23_002A_T_20_0_2_009"
INVALID_PRODUCT_NAME = "M50-100-A-YW"


def validate_product_name(product_name):
    pattern = r"^[0-9]{2}_[0-9]{3}"
    return re.match(pattern, product_name)