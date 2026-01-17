import streamlit as st
import requests
import time

# 백엔드 API 주소
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Netflix Lite", page_icon="🍿", layout="wide")

# --- 헤더 섹션 ---
st.title("Netflix Lite: AI Movie Recommender")
st.markdown("당신의 시청 기록을 분석하여 **취향저격 영화**를 찾아드립니다.")
st.divider()

# --- 사이드바: 유저 로그인 ---
with st.sidebar:
    st.header("로그인")
    user_id = st.number_input("User ID를 입력하세요", min_value=1, max_value=610, value=1)
    
    if st.button("추천 받기"):
        st.session_state['clicked'] = True

# --- 메인 화면 ---
if st.session_state.get('clicked'):
    with st.spinner('AI가 당신의 취향을 분석 중입니다...'):
        try:
            # 1. API 호출
            start_time = time.time()
            response = requests.get(f"{API_URL}/recommend/{user_id}")
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if response.status_code == 200:
                recommendations = response.json()
                
                # 속도 자랑하기 (Redis 효과)
                if elapsed_time < 0.1:
                    st.success(f"⚡ **Redis Cache Hit!** (0.0{int(elapsed_time*1000)}초 소요)")
                else:
                    st.info(f"🐢 **AI Model Inference** ({elapsed_time:.2f}초 소요)")

                st.subheader(f"User {user_id}님을 위한 추천 영화 TOP 10")
                
                # 2. 영화 카드 배치 (5개씩 2줄)
                # Streamlit의 columns 기능을 활용해 그리드 만들기
                for i in range(0, 10, 5): # 0, 5 (두 번 반복)
                    cols = st.columns(5) # 5개의 컬럼 생성
                    for j in range(5):
                        if i + j < len(recommendations):
                            movie = recommendations[i + j]
                            with cols[j]:
                                # 영화 제목이 너무 길면 자르기
                                title = movie['title']
                                if len(title) > 20:
                                    title = title[:17] + "..."
                                
                                # 카드 디자인
                                st.markdown(f"""
                                <div style="
                                    padding: 10px;
                                    border-radius: 10px;
                                    border: 1px solid #ddd;
                                    background-color: #262730;
                                    color: white;
                                    height: 200px;
                                    display: flex;
                                    flex-direction: column;
                                    justify-content: space-between;
                                ">
                                    <h4 style="margin:0;">🎬 {title}</h4>
                                    <p style="font-size:12px; color:#aaa;">{movie['genres'].replace('|', ', ')}</p>
                                    <div style="margin-top:10px;">
                                        <span style="font-size:20px; font-weight:bold; color:#E50914;">
                                            {int(movie['predicted_score'] * 20)}%
                                        </span>
                                        <span style="font-size:12px;">일치</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                    st.write("") # 줄바꿈 여백
            else:
                st.error("서버 연결에 실패했습니다.")
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")
            st.warning("백엔드 서버(uvicorn)가 켜져 있는지 확인해주세요!")

else:
    st.info("왼쪽 사이드바에서 User ID를 입력하고 추천 버튼을 눌러보세요!")