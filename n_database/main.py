from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    # 매번 세션 인스턴스가 생성됨
    db = SessionLocal()
    try:         # yield: 제네레이터
        yield db # db를 반환하고, 바깥의 코드가 끝나면 yield아래의 코드를 실행함.
    finally:     # finally: try 안의 코드가 성공하든 못하든 아래의 실행하고 끝냄
        db.close()


@app.post("/users/", response_model=schemas.User) # orm-mode가 켜진 스키마를 response_model에 넣어줘서 sqlAlchemy model를 response해줘도 알아서 처리해줌.
def create_user(user: schemas.UserCreate, # basemodel을 상속하는 클래스/ requsetbody에서 받아옴
                db: Session = Depends(get_db)):
    # sqlAlchemy는 async await를 못씀 / 쓰고싶으면 참고 https://fastapi.tiangolo.com/advanced/async-sql-databases/
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
