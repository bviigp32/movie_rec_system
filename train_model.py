import pandas as pd
import pickle
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate

from database import engine

# 모델을 저장할 파일 이름
MODEL_PATH = "recommendation_model.pkl"

def train_recommender():
    print("DB에서 평점 데이터를 불러오는 중...")
    
    # 1. DB에서 데이터 가져오기 (SQLAlchemy Engine 사용)
    # 필요한 컬럼: user_id, movie_id, score
    query = "SELECT user_id, movie_id, score FROM ratings"
    df = pd.read_sql(query, engine)
    
    print(f"총 {len(df)}개의 평점 데이터를 확보했습니다.")
    
    # 2. Surprise 라이브러리용 데이터로 변환
    # rating_scale: 평점의 범위 (0.5점 ~ 5.0점)
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df[['user_id', 'movie_id', 'score']], reader)
    
    # 3. SVD 알고리즘으로 모델 학습
    print("AI 모델 학습을 시작합니다... (SVD 알고리즘)")
    algo = SVD()
    
    # 학습 데이터 전체를 사용해 학습 (build_full_trainset)
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    
    # 성능 검증: 교차 검증 (RMSE 점수 확인용)
    print("모델 성능 검증 중 (Cross Validation)...")
    cv_results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    mean_rmse = cv_results['test_rmse'].mean()
    print(f"평균 RMSE(오차): {mean_rmse:.4f}")

    # 4. 모델 파일로 저장 (Serialization)
    print("학습된 모델을 파일로 저장합니다...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(algo, f)
        
    print(f"모델 저장 완료! -> {MODEL_PATH}")

if __name__ == "__main__":
    train_recommender()