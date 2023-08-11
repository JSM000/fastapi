from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = "root"
pwd = "1234" # 특수기호 전처리
host = "127.0.0.1"
port = 3306
db_url = f'mysql+pymysql://{user}:{quote(pwd)}@{host}:{port}/prac2'

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()