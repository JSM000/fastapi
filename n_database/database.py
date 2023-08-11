from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlalchemy은 orm을 위한 도구이고
# pymysql이 데이터베이스 클라이언트임
user = "root"
pwd = "1234" # 특수기호 전처리
host = "127.0.0.1"
port = 3306
db_url = f'mysql+pymysql://{user}:{quote(pwd)}@{host}:{port}/prac'

engine = create_engine(db_url)
# 세션: 일정 시간동안 같은 사용자로 부터 들어오는 일련의 요구를 하나의 상태로 보고 
# 그 상태를 일정하게 유지시키는 기술 (쿠키와 비슷)
# SQLAlchemy 모듈중에 sessoin이 있어서 이름을 SessionLocal로 지음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM model을 만들때 상속시켜줄 클래스
Base = declarative_base()