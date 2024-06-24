import streamlit as st
import json
from typing import Any

def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

class States:
    @staticmethod
    def initialize():
        if "config" not in st.session_state:
            st.session_state.config = read_json("config.json")
            print("Initialized session state")
    
    @staticmethod
    def get(key : str) -> Any:
        States.initialize()
        value = st.session_state.config[key]
        if value is None:
            raise KeyError(f"Key {key} not found in session state")
        return value

    @staticmethod
    def set(key : str, value : Any):
        States.initialize()
        st.session_state.config[key] = value
        
    @staticmethod
    def items() -> dict:
        States.initialize()
        return st.session_state.config.items()
        
__all__ = ["States"]