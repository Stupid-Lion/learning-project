import os
import streamlit as st

# 폰트 파일 경로
font_path = 'Nanum_Gothic/NanumGothic-Bold.ttf'  # 상대 경로로 설정

# 경로 확인
absolute_path = os.path.abspath(font_path)

# 경로 출력
st.write(f"배포 환경 폰트 경로 확인: {absolute_path}")