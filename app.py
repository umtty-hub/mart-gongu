import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="우리동네 마트 공구 대장", layout="wide")

# 로직: 예약번호 세팅 [2026-02-20]
def get_reservation_id(nickname):
    numbers = re.findall(r'\d+', nickname)
    if numbers:
        return "".join(numbers) 
    return nickname 

if 'db' not in st.session_state:
    st.session_state.db = []

st.title("🛒 우리동네 마트 한눈에 공구")

tab1, tab2 = st.tabs(["📝 한눈에 주문하기", "🔍 내 주문 확인"])

# --- [1] 리스트형 주문 화면 ---
with tab1:
    st.subheader("📦 오늘 장보기 리스트")
    st.caption("원하는 상품의 수량을 조절하신 후 하단의 '주문하기' 버튼을 눌러주세요.")

    # 상품 리스트 정의 (여기에 상품을 계속 추가하시면 됩니다)
    # [2026-02-19] 공백 포함 상품명 반영
    products = [
        {"이름": "빵빠레 초코1", "가격": "1,500원"},
        {"이름": "신선 딸기 500g", "가격": "9,800원"},
        {"이름": "여성용품(생리대) 특가", "가격": "12,000원"},
        {"이름": "삼겹살 600g", "가격": "15,000원"},
        {"이름": "대란 30구", "가격": "6,500원"},
        {"이름": "라면 번들(5입)", "가격": "4,500원"}
    ]

    order_quantities = {}
    
    # 상품을 표 형태로 나열
    for p in products:
        col_name, col_price, col_qty = st.columns([2, 1, 1])
        with col_name:
            st.write(f"**{p['이름']}**")
        with col_price:
            st.write(p['가격'])
        with col_qty:
            # 수량 선택 (기본 0)
            order_quantities[p['이름']] = st.number_input("수량", min_value=0, value=0, key=f"qty_{p['이름']}", label_visibility="collapsed")

    st.divider()
    
    # 주문 결정 구간
    final_items = {k: v for k, v in order_quantities.items() if v > 0}
    
    if final_items:
        st.write("### 🛒 선택한 상품")
        for k, v in final_items.items():
            st.write(f"- {k} : {v}개")
        
        nickname = st.text_input("카카오톡 닉네임 입력 (필수)", placeholder="예: 홍길동1234")
        
        if st.button("🚀 위 내역으로 주문 확정하기"):
            if not nickname:
                st.error("닉네임을 입력해 주셔야 주문이 접수됩니다!")
            else:
                res_id = get_reservation_id(nickname)
                summary = ", ".join([f"{k}({v})" for k, v in final_items.items()])
                
                new_order = {
                    "주문시간": datetime.now().strftime("%m-%d %H:%M"),
                    "예약번호": str(res_id),
                    "닉네임": nickname,
                    "주문내역": summary,
                    "상태": "접수완료"
                }
                st.session_state.db.append(new_order)
                st.success(f"✅ 주문 완료! 예약번호는 [{res_id}] 입니다. 매장에서 닉네임을 말씀해 주세요.")
    else:
        st.info("상품 수량을 1개 이상 선택하시면 주문 버튼이 나타납니다.")

# --- [2] 조회 화면 ---
with tab2:
    st.subheader("🔍 내 주문 찾기")
    search_query = st.text_input("닉네임 또는 예약번호를 입력하세요")
    if search_query:
        my_orders = [o for o in st.session_state.db if o['닉네임'] == search_query or o['예약번호'] == search_query]
        if my_orders:
            st.table(pd.DataFrame(my_orders)[["주문시간", "예약번호", "주문내역", "상태"]])
        else:
            st.warning("내역이 없습니다. 정보를 확인해 주세요.")

# --- 사장님 관리 도구 ---
st.markdown("---")
with st.expander("🔐 사장님 관리 도구"):
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 엑셀로 한꺼번에 다운로드", data=csv, file_name='today_orders.csv')
    else:
        st.write("접수된 주문이 아직 없습니다.")
