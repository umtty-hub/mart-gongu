import streamlit as st
import pandas as pd
import re
from datetime import datetime

# --- 설정 및 스타일 ---
st.set_page_config(page_title="우리동네 마트 공구 대장", layout="wide")

# --- 로직: 지침에 따른 예약번호 세팅 ---
def get_reservation_id(nickname):
    # 닉네임에서 숫자만 추출
    numbers = re.findall(r'\d+', nickname)
    if numbers:
        return "".join(numbers) 
    return nickname 

# --- 주문 데이터 저장소 ---
if 'db' not in st.session_state:
    st.session_state.db = []

# --- [1] 사용자 주문 화면 ---
st.title("🛒 우리동네 마트 실시간 공구")
st.info("카톡 닉네임을 입력하고 원하는 상품을 주문하세요!")

col1, col2 = st.columns([1, 1])

with col1:
    with st.form("order_form", clear_on_submit=True):
        st.subheader("📝 주문서 작성")
        # 상품명 리스트
        product_list = ["빵빠레 초코1", "신선 딸기 500g", "여성용품(생리대) 특가", "삼겹살 600g"]
        product = st.selectbox("상품을 선택하세요", product_list)
        
        nickname = st.text_input("카카오톡 닉네임 (입력 필수)", placeholder="예: 홍길동1234")
        qty = st.number_input("수량 (개)", min_value=1, value=1)
        
        submit = st.form_submit_button("공구 참여하기")
        
        if submit:
            if not nickname:
                st.error("닉네임을 입력해야 주문이 가능합니다!")
            else:
                res_id = get_reservation_id(nickname)
                order_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                new_order = {
                    "주문시간": order_time,
                    "예약번호": res_id,
                    "닉네임": nickname,
                    "상품명": product.strip(),
                    "수량": qty,
                    "상태": "대기"
                }
                st.session_state.db.append(new_order)
                st.success(f"✅ 주문 완료! 예약번호는 [{res_id}] 입니다.")

# --- [2] 사장님 전용 관리자 화면 ---
st.markdown("---")
with st.expander("🔐 사장님 전용 관리 도구"):
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        st.write(f"현재 총 {len(df)}건의 주문이 있습니다.")
        st.table(df)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 주문 내역 엑셀 다운로드",
            data=csv,
            file_name=f'mart_orders_{datetime.now().strftime("%m%d")}.csv',
            mime='text/csv',
        )
    else:
        st.write("아직 접수된 주문이 없습니다.")
