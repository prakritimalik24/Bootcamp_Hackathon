# RADIX Talent Match

RADIX Talent Match is a candidate-first career readiness tool built for the RADIX Talent Match Hackathon. It helps a student understand how their current skills compare with the RADIX 12-skill competency framework and with the requirements of a specific job.

The project brings together job-description analysis, resume signals, a student profile, readiness checking, and job-specific skill matching in one flow.

## Problem

Students often know the role they want, but not the exact skills they need to improve before applying. A resume alone does not show readiness clearly.

RADIX Talent Match turns the 12-skill framework into a practical view of a candidate's current level, their gaps, and the next skills to focus on.

## Modules

### 1. JD Analytics

Identifies the skill requirements from a job description.

### 2. Resume Parsing

Extracts skills and technical signals from a candidate's resume.

### 3. Profile Builder

Lets a student create a profile, add skills and projects, set proficiency levels for multiple skills, and attach optional evidence such as a GitHub link or certificate.

### 4. Talent Check

Shows readiness against a target role using the RADIX competency framework. It compares saved proficiency levels with the minimum level needed for the role.

### 5. Skill Matching

Matches one student against one specific job posting. The user selects the skills required for the job and the expected level for each skill. The module then shows:

- overall match score
- skills that meet the requirement
- skill gaps
- recommended focus areas

## Candidate Flow

1. Pick a job description.
2. Parse a resume.
3. Create or update the candidate profile.
4. Run Talent Check for role-level readiness.
5. Run Skill Matching for the selected job posting.

## Tech Stack

- Python
- Streamlit
- Supabase
- GitHub

## Running the Project

Clone the repository and open the project folder.

```bash
git clone https://github.com/prakritimalik24/Bootcamp_Hackathon.git
cd Bootcamp_Hackathon
```

Install the required packages:

```bash
pip install streamlit supabase
```

Create `.streamlit/secrets.toml` and add the Supabase credentials:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

Start the Streamlit app:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Database Tables Used

- `Profiles` — candidate details, self-reported skills, education, and experience
- `skill_set_master` — RADIX 12-skill competency framework
- `student_skill_levels` — proficiency level for each candidate and skill
- `skill_evidence` — optional portfolio, project, GitHub, or certificate evidence

## Team

**Team talenciaglobal**

Built for the RADIX Talent Match Hackathon.
