import streamlit as st
from session_state import States

def config_page():
    st.title("Config")
    st.write("This is the config page")

    model_options = ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]
    selected_model = st.selectbox(f"모델 선택", model_options)
    States.set('model', selected_model)

    # 슬라이더로 설정값 수정
    temperature = st.slider("Temperature", 0.0, 1.0, States.get('temperature'), 0.01)
    max_tokens = st.slider("Max Tokens", 100, 1000, States.get('max_tokens'), 1)
    top_p = st.slider("Top P", float(0.0), float(1.0), float(States.get('top_p')), float(0.01))
    frequency_penalty = st.slider("Frequency Penalty", float(0.0), float(2.0), float(States.get('frequency_penalty')), float(0.01))
    presence_penalty = st.slider("Presence Penalty", float(0.0), float(2.0), float(States.get('presence_penalty')), float(0.01))

    # 선택된 값들을 States에 저장
    States.set('model_name', selected_model)
    States.set('temperature', round(temperature, 2))
    States.set('max_tokens', max_tokens)
    States.set('top_p', round(top_p, 2))
    States.set('frequency_penalty', round(frequency_penalty, 2))
    States.set('presence_penalty', round(presence_penalty, 2))

    # 현재 설정값 전개
    st.write([f"{key}: {value:.2f}" if isinstance(value, (int, float)) else f"{key}: {value}" for key, value in States.items()])