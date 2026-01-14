import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def load_data():
    db = SessionLocal()
    
    try:
        # --- 1. Movies 데이터 적재 ---
        print("Movies 데이터를 읽는 중...")
        movies_df = pd.read_csv('data/movies.csv')
        
        print(f"{len(movies_df)}개의 영화 데이터를 DB에 저장합니다...")
        
        # DataFrame을 딕셔너리 리스트로 변환
        movies_data = []
        for _, row in movies_df.iterrows():
            movies_data.append(models.Movie(
                id=int(row['movieId']),
                title=row['title'],
                genres=row['genres']
            ))
            
        # 대량 데이터 한 번에 저장 (Bulk Insert)
        # 9000개 정도는 add_all로 한 번에 해도 괜찮습니다.
        db.add_all(movies_data)
        db.commit()
        print("Movies 저장 완료!")

        # --- 2. Users 데이터 적재 ---
        # ratings.csv에는 userId만 있고 Users 테이블은 비어있으므로,
        # 등장하는 모든 유저 ID를 먼저 Users 테이블에 등록해야 함.
        print("\nRatings 데이터를 읽어서 유저 정보를 추출 중...")
        ratings_df = pd.read_csv('data/ratings.csv')
        
        unique_users = ratings_df['userId'].unique()
        print(f"👤 {len(unique_users)}명의 유저를 DB에 저장합니다...")
        
        users_data = [models.User(id=int(user_id)) for user_id in unique_users]
        db.add_all(users_data)
        db.commit()
        print("Users 저장 완료!")

        # --- 3. Ratings 데이터 적재 ---
        print(f"\n{len(ratings_df)}개의 평점 데이터를 DB에 저장합니다... (시간이 좀 걸립니다)")
        
        # 10만 개는 한 번에 commit하면 무거울 수 있으니 배치 처리
        batch_size = 5000
        buffer = []
        
        for idx, row in ratings_df.iterrows():
            buffer.append(models.Rating(
                user_id=int(row['userId']),
                movie_id=int(row['movieId']),
                score=float(row['rating']),
                timestamp=int(row['timestamp'])
            ))
            
            if len(buffer) >= batch_size:
                db.add_all(buffer)
                db.flush() # 메모리 비우기 (commit은 나중에 한 번에 하거나 주기적으로)
                buffer = []
                print(f"   - {idx+1}개 처리 중...")
                
        # 남은 데이터 저장
        if buffer:
            db.add_all(buffer)
            
        db.commit()
        print("Ratings 저장 완료!")
        
    except Exception as e:
        print(f"에러 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 기존 데이터가 있다면 중복 에러가 날 수 있으니,
    # 테스트 단계에서는 테이블을 지웠다 다시 만드는 게 편함
    print("DB 초기화 중...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    load_data()