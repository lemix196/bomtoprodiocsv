import re

PRODUCT_TO_ORDER = ("23_002A_T_20_0_2_009",
                    "NC11LV",
                    "84")
PRODUCT_TO_PREPARE = ("18_064A_P_20_0_1_003",
                      "C45",
                      "Φ50"
                      )



class ProductValidator:
    def __init__(self, product_name: str, material: str, x_dimension: str) -> None:
        self.product_name = product_name
        self.material = material
        self.x_dimension = x_dimension


    def validate_product_name(self) -> bool:
        pattern = r"^[0-9]{2}_[0-9]{3}"
        return bool(re.match(pattern, self.product_name))


    def validate_material(self) -> str:
        MATERIALS_TO_ORDER = ["NC11LV",
                            "SLEIPNER",
                            "HOLDAX",
                            "VANADIS 4E"]
        
        MATERIALS_TO_PREPARE = ["S355",
                                "S235",
                                "C45"]
        
        MATERIALS_TO_OMIT = ["LASER2D"]
        
        if self.material.upper() in MATERIALS_TO_ORDER:
            return "order"
        elif self.material.upper()  in MATERIALS_TO_PREPARE:
            return "prepare"
        elif self.material.upper() in MATERIALS_TO_OMIT:
            return "omit"
        

    def validate_cylindricity(self) -> str:
        # check if first dimension is circular (starts with Φ symbol)
        if self.x_dimension[0] == chr(934):
            return True
        return False
    

    def validate_cylindrical_procedure(self):
            if not self.validate_cylindricity():
                return None
            if float(self.x_dimension[1:]) >= 50:
                return "prepare"
            else:
                return "ready"
    

    def validate_all(self):
        return (self.validate_product_name(),
                self.validate_material(),
                self.validate_cylindrical_procedure()
                )
    
