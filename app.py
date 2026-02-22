import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="우리동네 마트 공구 대장", layout="wide")

def get_reservation_id(nickname):
    numbers = re.findall(r'\d+', nickname)
    if numbers:
        return "".join(numbers) 
    return nickname 

if 'db' not in st.session_state:
    st.session_state.db = []

st.title("🛒 우리동네 마트 통합 주문서")
st.info("원하시는 상품들을 모두 체크한 후, 수량을 입력해 주세요!")

# --- [1] 사용자 주문 화면 ---
with st.form("multi_order_form", clear_on_submit=True):
    st.subheader("📝 주문 상품 선택")
    
    # 상품 리스트 (여성용품 등 품목 자유롭게 수정 가능)
    available_products = ["빵빠레 초코1", "신선 딸기 500g", "여성용품(생리대) 특가", "삼겹살 600g", "대란 30구"]
    
    # 다중 선택창
    selected_items = st.multiselect("구매하실 상품들을 모두 골라주세요", available_products)
    
    order_details = {}
    if selected_items:
        st.write("---")
        for item in selected_items:
            # 선택한 각 상품별로 수량 입력칸 생성
            order_details[item] = st.number_input(f"[{item}] 수량 선택", min_value=1, value=1, key=item)
    
    st.write("---")
    nickname = st.text_input("카카오톡 닉네임 (입력 필수)", placeholder="예: 홍길동1234")
    
    submit = st.form_submit_button("한 번에 주문하기")
    
    if submit:
        if not nickname:
            st.error("닉네임을 입력해야 주문이 가능합니다!")
        elif not selected_items:
            st.error("상품을 하나 이상 선택해 주세요!")
        else:
            res_id = get_reservation_id(nickname)
            order_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 여러 품목을 하나의 문자열로 정리 (예: 삼겹살(2), 딸기(1))
            summary = ", ".join([f"{k}({v})" for k, v in order_details.items()])
            
            new_order = {
                "주문시간": order_time,
                "예약번호": res_id,
                "닉네임": nickname,
                "주문내역": summary,
                "총품목수": len(selected_items),
                "상태": "대기"
            }
            st.session_state.db.append(new_order)
            st.success(f"✅ 주문 완료! 예약번호 [{res_id}]님, {len(selected_items)}개 품목이 접수되었습니다.")

# --- [2] 사장님 관리자 화면 ---
st.markdown("---")
with st.expander("🔐 사장님 전용 관리 도구"):
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        st.write(f"현재 총 {len(df)}건의 주문 묶음이 있습니다.")
        st.dataframe(df, use_container_width=True) # 표를 더 넓고 보기 좋게
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 전체 주문내역 엑셀 다운로드",
            data=csv,
            file_name=f'mart_summary_{datetime.now().strftime("%m%d")}.csv',
            mime='text/csv',
        )
    else:
        st.write("아직 접수된 주문이 없습니다.")
