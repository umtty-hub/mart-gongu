사장님, 제가 정말 큰 실수를 했네요! 코드 상자가 사장님 화면에서 안 보인다는 걸 깜빡하고 자꾸 상자에 담아 드렸습니다. 정말 죄송합니다. 얼마나 답답하셨을지 짐작도 안 가네요.

이번에는 특수 상자 하나도 없이, 그냥 제가 사장님께 보내는 일반 채팅 글자로 코드를 쫙 풀어드릴게요. 이 글자들은 무조건 보이실 겁니다.

🛠️ [여기서부터 끝까지 싹 복사해서 붙여넣으세요]
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="마트 주문판", layout="wide")

URL = "https://docs.google.com/spreadsheets/d/1a4UxIF3umGoGF4ZWc7BjwuMEiXj2NG5OFn7TO5H3lb4/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
df_p = conn.read(spreadsheet=URL, worksheet="products", ttl=0)
st.title("🛒 마트 초간편 주문")
t1, t2 = st.tabs(["📝 주문하기", "🔍 주문확인"])
