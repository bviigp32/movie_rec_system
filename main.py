from fastapi import FastAPI
import models
from database import engine

# DB 테이블 생성 (models.py의 내용을 보고 Postgres에 테이블을 만듦)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Netflix Lite API 🍿"}