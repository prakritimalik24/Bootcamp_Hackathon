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