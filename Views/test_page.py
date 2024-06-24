import streamlit as st


# version_type will be difined at main.py
def test_page(version_type : str):
    st.title("테스트")
    st.write("This is the test page")

    if version_type == "v1":
        st.write("This is the v1 test page")
    elif version_type == "v2":
        st.write("This is the v2 test page")
        
    