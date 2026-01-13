from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True) # movieId (데이터셋 값 사용)
    title = Column(String, index=True)
    genres = Column(String)

    # 역방향 관계 설정 (이 영화에 달린 평점들)
    ratings = relationship("Rating", back_populates="movie")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # userId
    # 실제 서비스라면 email, password가 있겠지만, 여기선 데이터셋의 ID만 사용
    
    ratings = relationship("Rating", back_populates="user")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True) # 고유 번호
    user_id = Column(Integer, ForeignKey("users.id"))  # 누가
    movie_id = Column(Integer, ForeignKey("movies.id")) # 어떤 영화를
    score = Column(Float)                              # 몇 점 줬나
    timestamp = Column(Integer)                        # 언제 (Unix Time)

    # 관계 설정 (rating.user 로 접근 가능하게)
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")