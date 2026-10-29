import streamlit as st

from db import get_profiles, get_skill_sets, get_student_skill_levels


def skill_matching_page():
    st.title("🧩 Skill Matching")
    st.write("Match one student's profile against one specific job posting.")

    try:
        profiles = get_profiles()
        skill_sets = get_skill_sets()
    except Exception as exc:
        st.error(f"Could not load matching data: {exc}")
        return

    if not profiles or not skill_sets:
        st.warning("Create a student profile and load the skill framework first.")
        return

    skill_names_by_id = {
        item["skill_set_id"]: item["skill_set_name"] for item in skill_sets
    }
    framework_skills = list(skill_names_by_id.values())

    student = st.selectbox(
        "Candidate",
        profiles,
        format_func=lambda item: (
            f"{item.get('name', 'Unnamed')} ({item.get('email', '')})"
        ),
    )

    st.subheader("Job Posting")
    job_title = st.text_input("Job title", placeholder="Backend Developer")
    company = st.text_input("Company", placeholder="Example: Google")
    required_skills = st.multiselect(
        "Skills required by this job posting",
        framework_skills,
        help="Choose the skills identified from the job description.",
    )

    required_levels = {}
    for skill in required_skills:
        required_levels[skill] = st.slider(
            f"Required level: {skill}",
            min_value=1,
            max_value=10,
            value=6,
            key=f"required_level_{skill}",
        )

    if not st.button("Run Skill Match", type="primary"):
        return

    if not job_title.strip():
        st.error("Enter a job title.")
        return
    if not required_skills:
        st.error("Select at least one skill required by the job posting.")
        return

    try:
        saved_levels = get_student_skill_levels(student.get("email", ""))
    except Exception as exc:
        st.error(f"Could not load the candidate's proficiency levels: {exc}")
        return

    candidate_levels = {
        skill_names_by_id.get(item["skill_set_id"]): item["proficiency_level"]
        for item in saved_levels
        if skill_names_by_id.get(item["skill_set_id"])
    }
    if not candidate_levels:
        st.warning("This candidate has no saved proficiency levels yet.")
        return

    ready, gaps, not_assessed = [], [], []
    for skill in required_skills:
        current = candidate_levels.get(skill)
        target = required_levels[skill]
        if current is None:
            not_assessed.append((skill, target))
        elif current >= target:
            ready.append((skill, current, target))
        else:
            gaps.append((skill, current, target))

    score = round(len(ready) / len(required_skills) * 100)
    company_label = f" at {company.strip()}" if company.strip() else ""
    st.subheader(f"Match for {job_title.strip()}{company_label}")
    score_col, ready_col, gap_col = st.columns(3)
    score_col.metric("Match Score", f"{score}%")
    ready_col.metric("Meets requirement", f"{len(ready)}/{len(required_skills)}")
    gap_col.metric("Gap skills", len(gaps) + len(not_assessed))
    st.progress(score / 100)

    st.subheader("Skill Gap List")
    for skill, current, target in ready:
        st.success(f"✅ {skill}: {current}/10 (job needs {target}/10)")
    for skill, current, target in gaps:
        st.warning(
            f"🟡 {skill}: {current}/10 (job needs {target}/10; improve by {target - current})"
        )
    for skill, target in not_assessed:
        st.error(f"🔴 {skill}: not assessed (job needs {target}/10)")

    if gaps or not_assessed:
        focus = [skill for skill, *_ in gaps + not_assessed]
        st.info("Recommended focus: " + ", ".join(focus))
    else:
        st.success("The candidate meets every selected job requirement.")
