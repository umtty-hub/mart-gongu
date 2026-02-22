import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="우리동네 마트 공구 대장", layout="wide")

# 로직: 지침에 따른 예약번호 세팅 [2026-02-20]
def get_reservation_id(nickname):
    numbers = re.findall(r'\d+', nickname)
    if numbers:
        return "".join(numbers) 
    return nickname 

if 'db' not in st.session_state:
    st.session_state.db = []

st.title("🛒 우리동네 마트 스마트 공구")

# 탭을 나눠서 주문하기와 내역 확인을 구분
tab1, tab2 = st.tabs(["📝 주문하기", "🔍 내 주문 확인"])

with tab1:
    with st.form("multi_order_form", clear_on_submit=True):
        st.subheader("주문서를 작성해 주세요")
        
        # [2026-02-19] 공백이 포함된 상품명도 정확히 처리
        available_products = ["빵빠레 초코1", "신선 딸기 500g", "여성용품(생리대) 특가", "삼겹살 600g", "대란 30구"]
        selected_items = st.multiselect("상품 선택", available_products)
        
        order_details = {}
        if selected_items:
            for item in selected_items:
                order_details[item] = st.number_input(f"[{item}] 수량", min_value=1, value=1, key=f"order_{item}")
        
        nickname = st.text_input("카카오톡 닉네임 입력", placeholder="예: 홍길동1234")
        submit = st.form_submit_button("주문 완료")
        
        if submit:
            if not nickname:
                st.error("닉네임을 입력해 주세요!")
            elif not selected_items:
                st.error("상품을 선택해 주세요!")
            else:
                res_id = get_reservation_id(nickname)
                summary = ", ".join([f"{k}({v})" for k, v in order_details.items()])
                
                new_order = {
                    "주문시간": datetime.now().strftime("%m-%d %H:%M"),
                    "예약번호": res_id,
                    "닉네임": nickname,
                    "주문내역": summary,
                    "상태": "접수완료"
                }
                st.session_state.db.append(new_order)
                st.success(f"✅ 주문 완료! 예약번호는 [{res_id}] 입니다.")

with tab2:
    st.subheader("내 주문 내역 찾기")
    search_nick = st.text_input("주문 시 입력한 닉네임을 입력하세요")
    
    if search_nick:
        # 입력한 닉네임과 일치하는 데이터만 필터링
        my_orders = [o for o in st.session_state.db if o['닉네임'] == search_nick]
        
        if my_orders:
            st.write(f"✨ {search_nick}님의 주문 내역입니다.")
            st.table(pd.DataFrame(my_orders)[["주문시간", "주문내역", "상태"]])
        else:
            st.warning("입력하신 닉네임으로 된 주문 내역이 없습니다.")

# --- 사장님 전용 관리 도구 (비공개 처리 권장) ---
st.markdown("---")
with st.expander("🔐 사장님 관리 도구"):
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 엑셀 다운로드", data=csv, file_name='orders.csv')
    else:
        st.write("주문이 없습니다.")
