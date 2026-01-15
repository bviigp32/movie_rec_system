# Netflix Lite: 개인화 영화 추천 시스템

사용자의 영화 평점 데이터를 기반으로 취향을 분석하고, 머신러닝(Collaborative Filtering)을 통해 맞춤형 영화를 추천해주는 추천 시스템 프로젝트입니다.

## 프로젝트 진행 로그
* **Day 1**: 프로젝트 환경 구축 및 DB 설계 (PostgreSQL, Redis, Docker Compose)
* **Day 2**: ETL 파이프라인 구축 (MovieLens 데이터셋 10만 건 DB 적재)
* **Day 3**: SVD 협업 필터링 모델 학습 및 저장 (.pkl)

## 기술 스택 (Tech Stack)
* **Language**: Python 3.11
* **Framework**: FastAPI
* **Database**: PostgreSQL (RDB), Redis (Cache)
* **ML Library**: Scikit-Learn, Surprise
* **Infra**: Docker, Docker Compose
* **Data Engineering**: Pandas (ETL)
* **AI Model**: SVD (Matrix Factorization)

## 데이터베이스 설계 (ERD)
* **User**: 사용자 정보
* **Movie**: 영화 메타데이터 (제목, 장르)
* **Rating**: 사용자-영화 간의 평점 및 관계 (N:M 관계 해소)

## 주요 기능 (Key Features)
1. **ETL 데이터 파이프라인**
   - Pandas를 활용해 CSV 파일에서 데이터 추출 및 전처리
   - SQLAlchemy Bulk Insert를 통해 대용량 데이터 고속 적재
2. **AI 추천 모델 학습**
   - Scikit-Surprise 라이브러리의 SVD 알고리즘 활용
   - 학습된 모델을 Pickle로 직렬화하여 API 서빙 최적화

---
*Dev Log: 매일 기능을 추가하며 업데이트 중입니다.*