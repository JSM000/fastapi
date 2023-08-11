from pydantic import BaseModel

class StudentBase(BaseModel): 
    num: str
    name: str
    ismale: bool

class StudentCreate(StudentBase): 
    pass                   

class Student(StudentBase):       
    id: int                 
    userr_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel): 
    email: str
    social_id: str| None = None
    nickname: str| None = None
    birthday: int | None = None
    last_login: int| None = None
    joined_at: int| None = None
    avartar_sgv: str| None = None
    is_active: bool| None = None
    is_superuser: bool| None = None
    is_male: bool| None = None

class UserCreate(UserBase): 
    password: str                   

class User(UserBase):       
    id: int                 
    school_id: int
    students: list[Student] = []
    class Config:
        orm_mode = True

class SchoolBase(BaseModel): 
    code: int
    area_code: str
    name: str

class SchoolCreate(SchoolBase): 
    pass                   

class School(SchoolBase):       
    id: int  
    user: list[User] = []
    class Config:
        orm_mode = True