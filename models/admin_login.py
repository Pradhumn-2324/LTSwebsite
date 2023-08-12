from pydantic import BaseModel

class admin_log(BaseModel):
    username : str
    password : str



class Employee(BaseModel):
    name: str
    gender: str
    contact_number: str
    emergency_contact: str
    email: str
    address: str
    dob: str
    password: str
    designation: str
    employee_type: str
    skills: str
    joining_date: str
