import streamlit as st
from session_state import States
from Views import config_page, test_page

def main():
    st.sidebar.title("윤선생 AI 튜터 테스트")
    choose_page = st.sidebar.selectbox("선택", ["퀴즈", "설정"])
    
    if choose_page == "퀴즈":
        test_page()
    elif choose_page == "설정":
        config_page()

if __name__ == "__main__":
    main()