import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

1. 앱 페이지 설정
st.set_page_config(page_title="우리동네 마트 초간편 주문판", layout="wide")

2. 사장님 구글 시트 주소
SHEET_URL = ""

3. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

try:
# 상품 리스트 가져오기 (실시간 반영)
df_products = conn.read(spreadsheet=SHEET_URL, worksheet="products", ttl=0)

except Exception as e:
st.error(f"⚠️ 시트 연결 오류: {e}")
