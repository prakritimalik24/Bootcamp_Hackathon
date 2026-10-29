import streamlit as st
from profile_builder import profile_page

st.set_page_config(
    page_title="AI Career Platform",
    page_icon="🎯",
    layout="wide"
)

profile_page()
