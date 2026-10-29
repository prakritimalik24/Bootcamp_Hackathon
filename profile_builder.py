import streamlit as st
from db import save_profile

def profile_page():
    st.title("🎓 Student Profile Builder")
    st.write("Create your professional profile")

    with st.form("profile_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        education = st.text_input("Education")
        skills = st.text_input(
            "Skills (comma separated)",
            placeholder="Python, SQL, Excel"
        )
        experience = st.text_area(
            "Experience / Projects"
        )

        submitted = st.form_submit_button(
            "Save Profile"
        )

    if submitted:
        if not name.strip() or not email.strip():
            st.error("Please enter your name and email.")
            return

        skill_list = [
            s.strip().lower()
            for s in skills.split(",")
            if s.strip()
        ]

        profile = {
            "name": name.strip(),
            "email": email.strip(),
            "education": education,
            "skills": skill_list,
            "experience": experience
        }

        try:
            save_profile(profile)
            st.success("Profile saved successfully! 🎉")
            st.balloons()
        except Exception as e:
            st.error(f"Error saving profile: {e}")