import streamlit as st

from db import get_profiles, get_skill_sets, get_student_skill_levels


# Each role uses the bootcamp's skill framework and a minimum proficiency level.
ROLE_REQUIREMENTS = {
    "Data Analyst": {"Coding": 5, "Aptitude and Problem Solving": 5,
                     "Communication Skills": 5, "AI Native Engineering": 5,
                     "SQL and Design": 7},
    "Web Developer": {"Coding": 6, "Communication Skills": 5,
                      "Object-Oriented Programming and Design": 6,
                      "Software Engineering": 6},
    "AI/ML Engineer": {"Coding": 7, "Data Structures and Algorithms": 6,
                       "AI Native Engineering": 8, "SQL and Design": 5},
    "Backend Developer": {"Coding": 7, "Data Structures and Algorithms": 6,
                          "Object-Oriented Programming and Design": 7,
                          "SQL and Design": 6,
                          "System Design and Architecture": 6,
                          "Software Engineering": 6},
    "DevOps Engineer": {"Coding": 5, "DevOps and Cloud": 7,
                         "System Design and Architecture": 6,
                         "Computer Networking": 5, "Operating System": 5},
}



def talent_page():
    st.title("🎯 Skill Matching")
    st.write("See how your saved proficiency levels match a target role.")

    try:
        profiles = get_profiles()
        skill_sets = get_skill_sets()
    except Exception as exc:
        st.error(f"Could not load skill-matching data: {exc}")
        return

    if not profiles:
        st.warning("Please create a profile first.")
        return
    if not skill_sets:
        st.warning("No skills were found in the bootcamp framework.")
        return

    profile = st.selectbox(
        "Select Student Profile", profiles,
        format_func=lambda item: (
            f"{item.get('name', 'Unnamed')} ({item.get('email', '')})"
        ),
    )
    role = st.selectbox("Select Target Job Role", list(ROLE_REQUIREMENTS))

    skill_names_by_id = {
        item["skill_set_id"]: item["skill_set_name"] for item in skill_sets
    }
    requirements = ROLE_REQUIREMENTS[role]
    unavailable = set(requirements) - set(skill_names_by_id.values())
    if unavailable:
        st.error(
            "These role skills are missing from skill_set_master: "
            + ", ".join(sorted(unavailable))
        )
        return

    try:
        saved_levels = get_student_skill_levels(profile.get("email", ""))
    except Exception as exc:
        st.error(f"Could not load this student's proficiency levels: {exc}")
        return

    student_levels = {
        skill_names_by_id.get(item["skill_set_id"]): item["proficiency_level"]
        for item in saved_levels
        if skill_names_by_id.get(item["skill_set_id"])
    }
    if not student_levels:
        st.info(
            "No proficiency levels have been saved for this student yet. "
            "Add them in Profile Builder first."
        )
        return

    matched, developing, missing = [], [], []
    for skill, required_level in requirements.items():
        current_level = student_levels.get(skill)
        if current_level is None:
            missing.append((skill, required_level))
        elif current_level >= required_level:
            matched.append((skill, current_level, required_level))
        else:
            developing.append((skill, current_level, required_level))

    total = len(requirements)
    score = round(len(matched) / total * 100)
    st.subheader(f"{role} Readiness")
    metric_col, matched_col, gap_col = st.columns(3)
    metric_col.metric("Skill Match", f"{score}%")
    matched_col.metric("Role-ready skills", f"{len(matched)}/{total}")
    gap_col.metric("Skills to improve", len(developing) + len(missing))
    st.progress(score / 100)

    st.subheader("Role Skill Match")
    for skill, required_level in requirements.items():
        current_level = student_levels.get(skill)
        if current_level is None:
            st.error(f"{skill}: not assessed — target level {required_level}/10")
        elif current_level >= required_level:
            st.success(
                f"{skill}: level {current_level}/10 — meets target {required_level}/10"
            )
        else:
            st.warning(
                f"{skill}: level {current_level}/10 — target {required_level}/10"
            )

    st.subheader("💡 Next Steps")
    if matched and not developing and not missing:
        st.success(f"You meet every listed skill target for {role}.")
    else:
        focus_skills = [item[0] for item in developing + missing]
        st.info("Focus on: " + ", ".join(focus_skills))

    with st.expander("View all saved proficiency levels"):
        for skill, level in sorted(student_levels.items()):
            st.write(f"{skill}: {level}/10")
