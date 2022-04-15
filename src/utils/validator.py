from cerberus.validator import Validator
from src.utils.errors import BadRequestError

def validator(schema, data):
    validator = Validator(schema)
    if validator.validate(data) == False:
        BadRequestError(validator.errors)
