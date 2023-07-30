from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated

# requestBody를 받는 방법
# 겸사겸사 validation까지
class Item(BaseModel): # BaseModel을 상속받는 클래스 생성
    name: str
    description: str | None = None # str,None 둘다가능, 선택값, 안들어오면 None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post('/requestBody/')
async def requestBody(item: Item = None): # 변수의 타입을 위 클래스로 지정
    item_dict = {{"item_name": "Foo"}, {"item_name": "Bar"}}
    if item:
        item_dict.update(item.dict())
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# 여러개 사용가능
class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/multiBody/")
async def multiBody(
    item: Item, 
    user: User, 
    # Body()를 사용해 query가 아니라 request Body 임을 명시
    importance: Annotated[int, Body(gt=0)] = None
):
    results = {"item": item, "user": user, "importance": importance}
    return results
# request body를 아래처럼 변수 이름으로 묶어서 보내주어야 한다.
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 3
# }

# requestBody로 받을 변수가 하나일 떄 이를 변수 이름으로 묶어서 받고 싶다면 
@app.put("/embed/")
async def embed(item: Annotated[Item, Body(embed=True)]):
    return item
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }

# requestBody validation하는 방법
# filed는 pydantic에서 import함
# Query, Path, Body와 속성이 같음
class Field1(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/field/")
async def field(item: Annotated[Field1, Body(embed=True)]):
    return item

# list 내부 타입 선언
# # 최신 파이썬
#  - my_list: list[str]
# # 3.9 이전 버전
#  - from typing import List
#  - my_list: List[str]

# 중첩 모델(list, set, dic, model을 중첩..)
class Image(BaseModel):
    url: HttpUrl # pydantic에서 지원하는 type / https://docs.pydantic.dev/latest/usage/types/types/
    name: str

class Item2(BaseModel):
    list1: list[str] = []
    set1: set[str] = set()
    image: Image | None = None # pydantic model을 중첩
    image2: list[Image] | None = None 

class Offer(BaseModel):
    name: str
    description: str | None = None
    items: list[Item2] # pydantic model을 list 안으로

@app.put("/nested/")
async def nested(offers: list[Offer]): # 함수인자에서도 list 안으로 가능
    return offers


# json의 key값을 모르는 경우 dict를 사용함
# json의 key 값을 int로 받을 수도 있음
@app.post("/useDict/")
async def useDict(weights: dict[int, float]):
    return weights

# pydantic model에 example을 추가하는 방법 / docs에 추가됨
# Field < config < Body 순으로 강함.
# 여러개 선언하면 고를수 있게 뜸(안됌;;)
class Example(BaseModel):
    # 1. Feild에 추가 하는 방법 / Path, Query, Body...에서도 사용가능
    name: str = Field(examples=["Foo"])
    price: float | None = Field(default=None, examples=[111])
    # 2. 모델 자체에 추가하는 방법
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bar",
                    "price": 222,
                }
            ]
        }
    }

@app.put("/example/")
async def update_item(
    item: Annotated[ # 3. Body에 추가하는 방법
        Example, 
        Body(
            examples= [
                {
                    "name": "Baz",
                    "price": 333,
                },
                {
                    "name": "jsm",
                },
            ]
        ),
    ]
):
    return item