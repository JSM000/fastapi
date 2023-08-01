from fastapi import FastAPI, Response, status, HTTPException

app = FastAPI()

# 100+: "Information"
#  - 직접 사용하는 경우는 거의 없음 / 응답 본문이 없어야함
# 200+: "Successful"
#  - 200: 모든 것이 정상
#  - 201: 데이터베이스에 새 레코드를 생성
#  - 204: 클라이언트에 반환할 콘텐츠가 없음 / 응답에 본문이 없어야 함
# 300+: "Redirection"
#  - 본문이 있을 수도 있고 없을 수도 있음
#  - 304: "Redirection" 본문이 없어야 함
# 400+: "Client error" 
#  - 400: 클라이언트의 일반적인 오류   
#  - 404: "Not Found" 서버에 없는 경로
# 500+: "Server error"
#  - 직접 사용하는 경우는 거의 없음
#  - 애플리케이션 코드 또는 서버의 일부에서 문제가 발생하면 
#    자동으로 상태 코드 중 하나를 반환

# ------------------------------200+------------------------------

# 데코레이터에 status_code 선언
# 응답 성공시의 status code를 정의함
# status를 사용해 정의 가능
@app.post("/status_code/", status_code=203) #status..HTTP_200_OK)
async def status_code(name: str):
    return {"name": name}

# 중간에 status code를 바꾸고 싶은 경우
tasks = {"foo": "Listen to the Bar Fighters"}
@app.put("/change_status_code/{task_id}", status_code=status.HTTP_200_OK)
def change_status_code(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]

#------------------------------400+--------------------------------
# Handling Errors
# 중간에 HTTPException를 일으키면 됨 / raise(o) return (x)
# header를 넣을 수도 있음 (특별한 경우) 
items = {"foo": "The Foo Wrestlers"}
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There goes my error"})
    return {"item": items[item_id]}

# 이후는 exception을 custom 하는 방법 / 아직 몰라도 될듯.