import streamlit as st
from session_state import States
from Views import config_page, test_page
from quiz import generate_quiz_info

def main():
    st.sidebar.title("윤선생 AI 튜터 테스트")
    choose_page = st.sidebar.selectbox("선택", ["퀴즈", "설정"])
    
    if choose_page == "퀴즈":
        if States.get("quiz_info") is None:
            quiz_info = generate_quiz_info()
            States.set("quiz_info", quiz_info)
        test_page()
    elif choose_page == "설정":
        config_page()
    
    if st.sidebar.button("재시작"):
        States.set("quiz_info", None)
        st.rerun()

if __name__ == "__main__":
    main()