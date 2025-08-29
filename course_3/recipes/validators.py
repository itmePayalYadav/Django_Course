from pint import UnitRegistry
from pint.errors import UndefinedUnitError
from django.core.exceptions import ValidationError

valid_unit_measurements = [
    "gram", "kilogram",   
    "milliliter", "liter",
    "teaspoon", "tablespoon", "cup", 
    "piece", "slice", "pinch"  
]

def validate_unit_of_measure(value):
    ureg = UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError(f"{e}")
    except Exception:
        raise ValidationError(f"'{value}' is not a valid unit of measurement.")
