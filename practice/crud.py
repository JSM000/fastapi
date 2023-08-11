from sqlalchemy.orm import Session
import hashlib


from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    m = hashlib.sha256()
    m.update(user.password.encode('utf-8'))
    db_user = models.User(email=user.email, password=m.hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()