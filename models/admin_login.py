from pydantic import BaseModel

class admin_log(BaseModel):
    username : str
    password : str



