import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="마트 주문판", layout="wide")

URL = ""

conn = st.connection("gsheets", type=GSheetsConnection)

try:
df_p = conn.read(spreadsheet=URL, worksheet="products", ttl=0)
st.title("🛒 마트 초간편 주문")
t1, t2 = st.tabs(["📝 주문하기", "🔍 주문확인"])

except Exception as e:
st.error(f"⚠️ 연결 오류: {e}")
