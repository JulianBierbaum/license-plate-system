from pydantic import BaseModel, Field
import datetime


class User_Password(BaseModel):
    username: str = Field(...) # ... <- Pflichtfeld
    password: str # , min_length=2, max_length=2) <- könnte nützlich sein, wenn username nicht schon fix-fertig aus ad kommt und noch angelegt werdenb muss



class User_Return(BaseModel):
    username: str


class Token_Authenticate(BaseModel):
    token: str


class Token_Data(BaseModel):
    username: str
    exp: datetime.datetime


class Token_Response(BaseModel):
    access_token: str
    token_type: str
