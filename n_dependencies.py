from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

# 중복되는 코드를 각 api에 넣어줌.
# 코드중복, database연결, 보안, Auth 등등에 사용
# async 자유롭게 사용가능
# docs에도 이전과 똑같이 표시됨.
# dependencies 안에 dependencies를 넣어서 계층 구성가능
# 이를 활용해 권한 수준에 따라 접근 가능한 라우터를 지정해줄수 있음.
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Annotated도 변수에 저장해서 사용가능
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/AnnotatedInVariable/")
async def AnnotatedInVariable(commons: CommonsDep):
    return commons