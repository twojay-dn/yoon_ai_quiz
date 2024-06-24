import streamlit as st
from session_state import States
from Views import config_page, test_page

def main():
    st.sidebar.title("윤선생 AI 튜터 테스트")
    choose_page = st.sidebar.selectbox("선택", ["v1", "v2", "설정"])
    
    if choose_page == "v1":
        test_page(version_type="v1")
    elif choose_page == "v2":
        test_page(version_type="v2")
    elif choose_page == "설정":
        config_page()

if __name__ == "__main__":
    main()