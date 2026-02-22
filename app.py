import streamlit as st
from streamlit_gsheets import GSheetsConnection # 구글 시트 연결 도구
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="우리동네 마트 실시간 주문", layout="wide")

# [2026-02-20] 예약번호 로직
def get_reservation_id(nickname):
    numbers = re.findall(r'\d+', nickname)
    return "".join(numbers) if numbers else nickname

# 구글 시트 연결 설정
# 여기에 사장님의 구글 시트 주소를 넣으세요
SHEET_URL = "사장님의_구글_시트_주소_입력"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- 데이터 불러오기 ---
# 시트의 'products' 탭에서 상품 리스트를 가져옵니다.
df_products = conn.read(spreadsheet=SHEET_URL, worksheet="products")

st.title("🛒 우리동네 마트 시트 연동 주문판")

tab1, tab2 = st.tabs(["📝 주문하기", "🔍 내 주문 확인"])

with tab1:
    st.subheader("📦 오늘 장보기 리스트")
    order_quantities = {}
    
    # 시트에서 가져온 상품들을 화면에 나열
    for index, row in df_products.iterrows():
        col_name, col_price, col_qty = st.columns([2, 1, 1])
        with col_name: st.write(f"**{row['이름']}**")
        with col_price: st.write(str(row['가격']))
        with col_qty:
            order_quantities[row['이름']] = st.number_input("수량", min_value=0, value=0, key=f"q_{index}", label_visibility="collapsed")

    st.divider()
    final_items = {k: v for k, v in order_quantities.items() if v > 0}
    
    if final_items:
        nickname = st.text_input("카톡 닉네임 입력")
        if st.button("🚀 주문하기"):
            res_id = get_reservation_id(nickname)
            summary = ", ".join([f"{k}({v})" for k, v in final_items.items()])
            
            # 새 주문 데이터 생성
            new_order = pd.DataFrame([{
                "주문시간": datetime.now().strftime("%m-%d %H:%M"),
                "예약번호": str(res_id),
                "주문내역": summary,
                "상태": "접수완료"
            }])
            
            # 구글 시트의 'orders' 탭에 직접 추가!
            existing_orders = conn.read(spreadsheet=SHEET_URL, worksheet="orders")
            updated_orders = pd.concat([existing_orders, new_order], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, worksheet="orders", data=updated_orders)
            
            st.success(f"✅ 시트로 주문 전송 완료! 예약번호: {res_id}")
