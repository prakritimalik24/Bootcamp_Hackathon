import streamlit as st
from db import save_profile, save_skill_evidence, save_student_skill_level


# Preserve the skill IDs used by the existing database integration.
SKILL_NAMES = [
    "Coding",
    "Data Structures and Algorithms",
    "Aptitude and Problem Solving",
    "Communication Skills",
    "Object-Oriented Programming and Design",
    "AI Native Engineering",
    "SQL and Design",
    "System Design and Architecture",
    "DevOps and Cloud",
    "Software Engineering",
    "Computer Networking",
    "Operating System",
]
SKILL_IDS = {name: index + 1 for index, name in enumerate(SKILL_NAMES)}


def profile_page():
    st.title("🎓 Student Profile Builder")
    st.write("Create your professional profile")

    # Keep these widgets outside a form so selecting skills immediately
    # renders their individual sliders.
    name = st.text_input("Full Name", key="profile_name")
    email = st.text_input("Email Address", key="profile_email")
    education = st.text_input("Education", key="profile_education")
    skills = st.text_input(
        "Skills (comma separated)",
        placeholder="Python, SQL, Excel",
        key="profile_skills",
    )
    experience = st.text_area(
        "Experience / Projects", key="profile_experience"
    )

    st.subheader("📊 Skill Proficiency Assessment")
    selected_skills = st.multiselect(
        "Select the skills you want to assess",
        SKILL_NAMES,
        key="profile_assessment_skills",
    )
    skill_levels = {}
    for skill in selected_skills:
        skill_levels[skill] = st.slider(
            f"{skill} proficiency",
            min_value=1,
            max_value=10,
            value=1,
            key=f"profile_proficiency_{SKILL_IDS[skill]}",
        )

    st.subheader("🏆 Skill Evidence Vault")
    st.caption("Optional: add a link that demonstrates one of your skills.")
    evidence_skill = st.selectbox(
        "Which skill are you providing proof for?",
        ["No evidence", *SKILL_NAMES],
        key="profile_evidence_skill",
    )
    evidence_type = st.selectbox(
        "Evidence Type",
        ["github", "project", "certificate", "other"],
        key="profile_evidence_type",
    )
    evidence_url = st.text_input(
        "Evidence Link",
        placeholder="https://github.com/username/project",
        key="profile_evidence_url",
    )
    evidence_description = st.text_area(
        "What does this evidence demonstrate?",
        key="profile_evidence_description",
    )

    if not st.button("Save Profile", key="profile_save"):
        return

    if not name.strip() or not email.strip():
        st.error("Please enter your name and email.")
        return
    if evidence_skill == "No evidence" and evidence_url.strip():
        st.error("Select a skill for your evidence link, or clear the link.")
        return
    if evidence_skill != "No evidence" and not evidence_url.strip():
        st.error("Enter an evidence link, or select 'No evidence'.")
        return

    profile = {
        "name": name.strip(),
        "email": email.strip(),
        "education": education,
        "skills": [s.strip().lower() for s in skills.split(",") if s.strip()],
        "experience": experience,
    }

    stage = "profile"
    profile_saved = False
    try:
        save_profile(profile)
        profile_saved = True

        for skill, level in skill_levels.items():
            stage = f"proficiency for {skill}"
            save_student_skill_level(email.strip(), SKILL_IDS[skill], level)

        if evidence_skill != "No evidence" and evidence_url.strip():
            stage = "skill evidence"
            save_skill_evidence({
                "student_email": email.strip(),
                "skill_set_id": SKILL_IDS[evidence_skill],
                "evidence_type": evidence_type,
                "evidence_url": evidence_url.strip(),
                "evidence_description": evidence_description.strip(),
            })
    except Exception as exc:
        if profile_saved:
            st.error(
                f"Your profile was saved, but saving {stage} failed: {exc}. "
                "Some skill data may already have been saved."
            )
        else:
            st.error(f"Error saving profile: {exc}")
        return

    st.success("Profile saved successfully! 🎉")
    st.balloons()
