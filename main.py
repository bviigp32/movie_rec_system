import pickle
import json
import redis
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
import models

# 1. 인프라 연결 설정
# Redis 연결 (Docker 컨테이너 이름이 'movie-redis'가 아니라 로컬호스트로 접속)
# 이유: uvicorn을 내 컴퓨터에서 실행하니까 localhost:6379로 붙어야 함
rd = redis.Redis(host='localhost', port=6379, db=0)

# 2. 학습된 AI 모델 불러오기
# 서버 켤 때 한 번만 로딩 (메모리 절약)
MODEL_PATH = "recommendation_model.pkl"
print("AI 모델을 로딩 중입니다...")
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
print("모델 로딩 완료!")

# 3. 영화 목록 미리 로딩 (매번 DB 가면 느리니까)
print("영화 목록을 캐싱 중입니다...")
all_movie_ids = pd.read_sql("SELECT id FROM movies", engine)['id'].tolist()
print(f"총 {len(all_movie_ids)}개의 영화 ID 로딩 완료.")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Netflix Lite Recommendation API"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    특정 유저(user_id)에게 '아직 안 본 영화' 중 10개를 추천합니다.
    """
    cache_key = f"rec:{user_id}"

    # 1. Redis 캐시 확인
    cached_data = rd.get(cache_key)
    if cached_data:
        print(f"⚡ [Cache Hit] 유저 {user_id}의 추천 목록을 Redis에서 가져왔습니다.")
        return json.loads(cached_data)

    print(f"🐢 [Cache Miss] AI 모델이 유저 {user_id}의 취향을 분석 중...")

    # --- [업그레이드 된 로직 시작] ---
    
    # 2. 유저가 이미 본(평점을 남긴) 영화 ID 목록 가져오기
    # DB 쿼리: SELECT movie_id FROM ratings WHERE user_id = ...
    watched_list = db.query(models.Rating.movie_id).filter(models.Rating.user_id == user_id).all()
    # 가져온 리스트 [(1,), (50,), (100,)] 를 집합 {1, 50, 100} 으로 변환
    watched_movie_ids = {m[0] for m in watched_list}

    # 3. 안 본 영화만 남기기 (차집합 연산)
    # 전체 영화(set) - 본 영화(set) = 안 본 영화
    all_movie_set = set(all_movie_ids)
    unseen_movie_ids = all_movie_set - watched_movie_ids
    
    print(f"🔍 전체 {len(all_movie_ids)}개 중 유저가 안 본 {len(unseen_movie_ids)}개 영화만 예측합니다.")

    # 4. 안 본 영화에 대해서만 예측 수행
    predictions = []
    for movie_id in unseen_movie_ids:
        pred = model.predict(user_id, movie_id)
        predictions.append((movie_id, pred.est))
    
    # --- [업그레이드 된 로직 끝] ---

    # 5. 상위 10개 추출 (나머지는 동일)
    top_10 = sorted(predictions, key=lambda x: x[1], reverse=True)[:10]
    
    top_movie_ids = [m[0] for m in top_10]
    movies = db.query(models.Movie).filter(models.Movie.id.in_(top_movie_ids)).all()
    
    result = []
    for m in movies:
        score = next(item[1] for item in top_10 if item[0] == m.id)
        result.append({
            "movie_id": m.id,
            "title": m.title,
            "genres": m.genres,
            "predicted_score": round(score, 2)
        })

    rd.setex(cache_key, 3600, json.dumps(result))
    
    return result