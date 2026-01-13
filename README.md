# Netflix Lite: 개인화 영화 추천 시스템

사용자의 영화 평점 데이터를 기반으로 취향을 분석하고, 머신러닝(Collaborative Filtering)을 통해 맞춤형 영화를 추천해주는 추천 시스템 프로젝트입니다.

## 프로젝트 진행 로그
* **Day 1**: 프로젝트 환경 구축 및 DB 설계 (PostgreSQL, Redis, Docker Compose)

## 기술 스택 (Tech Stack)
* **Language**: Python 3.11
* **Framework**: FastAPI
* **Database**: PostgreSQL (RDB), Redis (Cache)
* **ML Library**: Scikit-Learn, Surprise
* **Infra**: Docker, Docker Compose

## 데이터베이스 설계 (ERD)
* **User**: 사용자 정보
* **Movie**: 영화 메타데이터 (제목, 장르)
* **Rating**: 사용자-영화 간의 평점 및 관계 (N:M 관계 해소)

---
*Dev Log: 매일 기능을 추가하며 업데이트 중입니다.*