from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

class Person(BaseModel):
    first_name: str
    last_name: str

    @field_validator('first_name', 'last_name')
    def names_must_be_capatilized(cls, val: str):
        if not val.istitle():
            raise ValueError("Names must be capitalized")


class User(BaseModel):
    email: str

    @field_validator('email')
    def normalized_email_address(cls, email_addr:str):
        return email_addr.lower().strip()

# Validations before using models

class Product(BaseModel):
    price:str # $4.5

    @field_validator('price', mode='before')
    def extract_price(cls, price):
        if isinstance(price,str):
            return float(price.replace('$', '').replace(',', ''))
        
class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def validate_date_range(cls, values):
        if values.start_date >=values.end_date:
            raise ValueError("End date must be after start date")
        return values