from typing import Annotated

from fastapi import FastAPI, Cookie, Header

app = FastAPI()

# -------------------------- cookie --------------------------------
@app.get("/cookie/")
async def cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# -------------------------- header --------------------------------
# 헤더에서는 보통 변수명에 "-"를 쓰는데 파이썬에서는 "-"은 변수로 선언 불가능
# fastapi가 자동으로 "-" <-> "_" 변경해줌
# 굳이 "_"를 쓰고싶으면 convert_underscores = False  (True가 default)
@app.get("/header/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None
):    
    return {"strange_header-Agent": strange_header}

# 중복된 헤더 값 받기
# X-Token: foo / X-Token: bar를 리스트로 받아줌
@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}