from enum import Enum
from fastapi import FastAPI , Path
from typing import Annotated

app = FastAPI()

# 경로는 순차적으로 검사 하기떄문에 
# 같은 경로에서 특정값을 경로로 선언하고 싶으면 먼저 선언해야함
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Path parm 받는 방법
# (Path param) : (type) 으로 타입도 선언 가능
@app.get('/pathParam/{item_id}')
async def pathParam(item_id: int):
    return {"item_id":item_id}

# Path parm의 값 validation하는 법 
# 열거형으로 정리된 값만 받고, 해당 값이 아니면 리턴값에 필요한 값이 표시됨. docs에도 표시됨
class PathModel(str, Enum):
    foo = "foo"
    bar = "bar"

@app.get("/pathModel/{name}")
async def pathModel(name: PathModel):
    if name is PathModel.foo:
        return {"name": name}
    if name.value == "lenet":
        return {"name": name}
    return {"name": name}

# 아래처럼 뛰엄뛰엄도 가능
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id}

# 파일경로(예:/home/johndoe/myfile.txt)를 Path pram으로 받는 경우
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}



#---------------------Validation--------------------------



# Path param도 query와 방법이 같음(예전방법도 가능)
# Path param은 무조건 필수이기 때문에 default를 지정하면 오류
# Path와 Query는 같은 클래스를 상속받기 때문에 속성값도 모두 같은 걸 사용함
@app.get("/path/{item_id}")
async def path(
    item_id: Annotated[
        int, 
        Path(
            min_length=3, 
            max_length=50, 
            pattern="^fixedquery$", # pattern : 정규식 추가 / 구버젼에서는 regex라고 사용
            title = "asefhbzskdfawkejf", # redoc에서 사용? doc에서는 못찾겠음.
            description="Query string ~~", # docs에 표시
            alias="item-query", # 별명 선언 / "q"는 사용 못하게 됨 "-"는 원래 파이썬 변수명으로 사용 못함
            deprecated=True, # 지원 중단된 쿼리임을 docs에 선언 / 동작은 함
            include_in_schema=True,# docs에서 표시되지 않도록 설정 / 동작은 함
            title="The ID of the item to get",
            ge = 0, # item_id >= 0
            gt = 0, # item_id > 0
            le = 0, # item_id <= 0
            lt = 0 # item_id < 0
        )
    ], 
    q:str
):
    return {"item_id": item_id}

# 예전방법(Annotated없이 사용)에서는 단순 Path()도 default값이라고 인식하기 때문에 default값을 설정하지 않아도 뒤쪽으로 적어야 했음.
# async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
# 앞에 *를 넣어주면 선택변수로 인식하지 않음
# async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
