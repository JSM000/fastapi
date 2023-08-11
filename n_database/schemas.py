# Pydantic models을 저장하기 위한 파일
# SQLAlchemy models과 비슷해서 따로 관리함
# database랑 값을 주고받을때 validation하기 위한 용도

from pydantic import BaseModel

class ItemBase(BaseModel): # 공통되는 속성을 담은 모델
    title: str
    description: str | None = None

class ItemCreate(ItemBase): # create할 때 쓰이는 모델
    pass                    # (이경우 별도의 추가 속성이 안쓰임)

class Item(ItemBase):       # read / return 할떄 쓰이는 모델
    id: int                 # creat할떄는 알 수 없는 값들
    owner_id: int

# 역할1. pydantic이 dict가 아니어도 읽을 수 있게 해줌. 
#        (data[id]가 아니라 data.id로도 읽을 수 있게 함.)
# 역할2. SQLAlchemy는 lazy loading이라서 user.item처럼 
#        직접 호출 해야지만 관계된 데이터를 불러옴.
#        orm_mode는 이것을 해결
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase): 
    password: str # password는 보안상 create 할때만 사용됨 
                  #read 해올 수 있으면 안됨
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


