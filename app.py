import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="마트 주문판", layout="wide")


URL = "https://docs.google.com/spreadsheets/d/1a4UxIF3umGoGF4ZWc7BjwuMEiXj2NG5OFn7TO5H3lb4/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
# 상품 읽기
df_p = conn.read(spreadsheet=URL, worksheet="products", ttl=0)

except Exception as e: st.error(f"오류발생: {e}")
