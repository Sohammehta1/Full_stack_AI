from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    is_active: bool = Field(alias='isActive')

input_data = {'id': 1, "name": 'chaiCode','isActive': True}

user= User(**input_data)

print(user)