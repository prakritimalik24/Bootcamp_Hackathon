import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def save_profile(data):
    return supabase.table("Profiles").insert(data).execute()

def get_profiles():
    return supabase.table("Profiles").select("*").execute().data

def save_skill_evidence(data):
    return supabase.table("skill_evidence").insert(data).execute()
def get_skill_sets():
    return (
        supabase.table("skill_set_master")
        .select("skill_set_id, skill_set_name")
        .order("skill_set_id")
        .execute()
        .data
    )
def get_student_skill_levels(email):
    return (
        supabase.table("student_skill_levels")
        .select("skill_set_id, proficiency_level")
        .eq("student_email", email)
        .execute()
        .data
    )
def save_student_skill_level(email, skill_set_id, level):
    return (
        supabase.table("student_skill_levels")
        .upsert(
            {
                "student_email": email,
                "skill_set_id": skill_set_id,
                "proficiency_level": level
            },
            on_conflict="student_email,skill_set_id"
        )
        .execute()
    )