import streamlit as st
from quiz import rand_pick, welcome_messages, correct_guess_messages, validate_answer, response_for_wrong_answer
import time
from session_state import States

if not st.session_state.get("turn_count"):
    st.session_state.turn_count = 1
if not st.session_state.get("turn_limit"):
    st.session_state.turn_limit = 20

def test_page():
    st.title("스무고개 테스트")
    
    is_end = False
    quiz_info = States.get("quiz_info")
    welcome_message = rand_pick(welcome_messages)
    right_message = rand_pick(correct_guess_messages).format(quiz_answer=quiz_info.quiz_answer)
    if not st.session_state.get("chat_history"):
        st.session_state["chat_history"] = []
    if len(st.session_state["chat_history"]) == 0:
        st.session_state["chat_history"].append({"role" : "assistant", "content" : welcome_message})
    
    tab1, tab2 = st.tabs(["힌트와 정답", "퀴즈"])
    user_input = None

    with tab1:
        st.write("힌트와 정답")
        st.write(f"생성된 정답 : {quiz_info.quiz_answer}")
        st.write("생성된 힌트 :")
        for hint in quiz_info.quiz_hint:
            st.write(hint)

    with tab2:
        # 여기서 채팅 입력창을 하단에 배치합니다.
        # 다른 컨텐츠를 위쪽에 배치
        chat_history_container = st.container(height=450)
        input_container = st.container(height=100)

        if is_end or st.session_state.turn_count >= st.session_state.turn_limit:
            st.write("테스트가 종료되었습니다.")
            st.write(f"총 턴 수 : {st.session_state.turn_count} / {st.session_state.turn_limit} 입니다.")
        
        with input_container:
            user_input = st.chat_input("type...")
            st.write(f"턴 수 : {st.session_state.turn_count} / {st.session_state.turn_limit}")
            if user_input is not None:
                st.session_state["chat_history"].append({"role" : "user", "content" : user_input})
                if validate_answer(quiz_info.quiz_answer, user_input):
                    time.sleep(1)
                    st.session_state["chat_history"].append({"role" : "assistant", "content" : right_message})
                    is_end = True
                elif st.session_state.turn_count < st.session_state.turn_limit:
                    res = response_for_wrong_answer(quiz_info, user_input)
                    print(res)
                    st.session_state["chat_history"].append({"role" : "assistant", "content" : res.content})
                    st.session_state.turn_count += 1
                else:
                    st.session_state["chat_history"].append({"role" : "assistant", "content" : "턴 수가 모두 소진되었습니다. 종료합니다."})

        with chat_history_container:
            for message in st.session_state["chat_history"]:
                st.write(f"{message['role']} : {message['content']}")