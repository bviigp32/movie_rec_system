FROM python:3.11-slim

WORKDIR /app

# apt-get은 리눅스의 '앱스토어' 같은 명령어입니다.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 필수 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 실행 명령어 (docker-compose에서 덮어씌워짐)
CMD ["bash"]