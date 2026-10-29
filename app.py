import streamlit as st
from profile_builder import profile_page
from talent_check import talent_page
from skill_matching import skill_matching_page

st.set_page_config(
    page_title="Career Platform",
    page_icon="🎯",
    layout="wide"
)

st.sidebar.title("🎯 Career Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Profile Builder", "Talent Check", "Skill Matching"]
)

if page == "Profile Builder":
    profile_page()

elif page == "Talent Check":
    talent_page()

elif page == "Skill Matching":
    skill_matching_page()
