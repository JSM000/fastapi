from fastapi import FastAPI, Query
from typing import Annotated
from typing import Union

app = FastAPI()

# query 받는 방법: Path pram에 없는 변수를 선언
# http://127.0.0.1:8000/items/?skip=0&limit=10
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/queryParam/{user_id}")
async def queryParam(user_id: str, skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 쿼리를 선택값으로 설정하는 방법
# 함수의 매개변수는 필수변수를 선택변수 앞쪽에 적어야함. / Path는 항상 필수변수이므로 제일 앞에
@app.get("/unrequired/")
async def unrequired(
    needy: str,         # required 쿼리   / 생략하면 필수변수(보통 이렇게 사용) = ... (필수변수임을 표시, 굳이 안씀)
    choose: str = None, # unrequired 쿼리 / = None (선택변수, 안들어오면 None) ="asd" (선택변수, 안들어오면 "asd")
    union: Union[str, None] = "asd", # 여러개의 타입 선언 방법/ python 최신버젼에서는 str | None
    boolean: bool = False # boolean 타입 선언 / 1,True,true,on,yes => True
):
    item = {"needy": needy}
    if choose:
        item.update({"q": choose})
    if not boolean:
        item.update(
            {"description": "This is an amazing item"}
        )
    return item



#---------------------Validation--------------------------



# 쿼리에 validation과 metadata를 추가 하는 방법
# 예전 방법 : q: str | None = Query(default=None, max_length=50)
@app.get("/query/")
async def query(
    q: Annotated[
        str | None, 
        Query(
            min_length=3, # 길이의 최솟값 / 문자열일떄만 사용가능
            max_length=50, # 길이의 최대값 / 문자열일떄만 사용가능
            pattern="^fixedquery$", # pattern : 정규식 추가 / 구버젼에서는 regex라고 사용
            title = "asefhbzskdfawkejf", # redoc에서 사용? doc에서는 못찾겠음.
            description="Query string ~~", # docs에 표시
            alias="item-query", # 별명 선언 / "q"는 사용 못하게 됨 "-"는 원래 파이썬 변수명으로 사용 못함
            deprecated=True, # 지원 중단된 쿼리임을 docs에 선언 / 동작은 함
            include_in_schema=True,# docs에서 표시되지 않도록 설정 / 동작은 함
            ge = 0, # item_id >= 0 / 숫자형일떄만 사용가능
            gt = 0, # item_id > 0 / 숫자형일떄만 사용가능
            le = 0, # item_id <= 0 / 숫자형일떄만 사용가능
            lt = 0 # item_id < 0 / 숫자형일떄만 사용가능
        ),
    ] = None
): 
    return q

# 쿼리로 리스트를 받는 방법 / 이렇게 전달 (http://localhost:8000/items/?q=foo&q=bar)
# Query() 없이 (q: list | None = None) 이렇게 하면 request body로 받음.
# list[str]로 리스트 안의 타입도 선언 가능
@app.get("/queryList/")
async def queryList(q: Annotated[list | None, Query()] = None):
    return {"q": q}