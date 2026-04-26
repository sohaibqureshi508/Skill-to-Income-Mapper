import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

# Optional AI (Groq)
USE_AI = False
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    USE_AI = True
except:
    USE_AI = False

# -----------------------------
# Core Skill Database (Deterministic)
# -----------------------------
SKILL_DB = {
    "python": {
        "next": ["machine learning", "data science", "backend development"],
        "freelance": ["automation scripts", "web scraping", "API development"],
        "jobs": ["Software Engineer", "Data Analyst"],
        "income_pk": (50000, 200000),
        "income_abroad": (3000, 9000)
    },
    "graphic design": {
        "next": ["ui/ux design", "branding", "motion graphics"],
        "freelance": ["logo design", "social media posts", "brand kits"],
        "jobs": ["UI Designer", "Creative Designer"],
        "income_pk": (40000, 150000),
        "income_abroad": (2000, 7000)
    },
    "web development": {
        "next": ["react", "full stack", "web3"],
        "freelance": ["website development", "landing pages", "bug fixing"],
        "jobs": ["Frontend Developer", "Full Stack Developer"],
        "income_pk": (60000, 250000),
        "income_abroad": (3500, 10000)
    },
    "digital marketing": {
        "next": ["seo", "performance marketing", "analytics"],
        "freelance": ["ads management", "content strategy", "SEO optimization"],
        "jobs": ["Marketing Specialist", "Growth Manager"],
        "income_pk": (50000, 180000),
        "income_abroad": (2500, 8000)
    }
}

# -----------------------------
# Helper Functions
# -----------------------------
def normalize_skill(skill):
    return skill.lower().strip()

def generate_skill_graph(base_skill, next_skills):
    fig = go.Figure()

    # central node
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        text=[base_skill],
        textposition="bottom center",
        marker=dict(size=30)
    ))

    # surrounding nodes
    angles = np.linspace(0, 2*np.pi, len(next_skills), endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers+text',
        text=next_skills,
        textposition="top center",
        marker=dict(size=20)
    ))

    fig.update_layout(
        title="Skill Progression Map",
        showlegend=False
    )

    return fig

def ai_enhancement(skill):
    if not USE_AI:
        return "AI enhancement not available (no API key)."

    prompt = f"""
    Skill: {skill}
    Provide:
    1. Advanced monetization strategies
    2. High-income niches
    3. Future demand outlook
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Skill to Income Mapper", layout="wide")

st.title("💡 Skill-to-Income Mapper")
st.markdown("Enter your skill to explore earning potential, career paths, and growth roadmap.")

skill_input = st.text_input("Enter your skill (e.g., Python, Graphic Design):")

if skill_input:
    skill = normalize_skill(skill_input)

    if skill in SKILL_DB:
        data = SKILL_DB[skill]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Income Scope")

            st.markdown(f"**Pakistan:** PKR {data['income_pk'][0]:,} – {data['income_pk'][1]:,}")
            st.markdown(f"**Abroad (USD/month):** ${data['income_abroad'][0]} – ${data['income_abroad'][1]}")

        with col2:
            st.subheader("💼 Opportunities")

            st.markdown("**Freelance:**")
            for f in data["freelance"]:
                st.write(f"- {f}")

            st.markdown("**Jobs:**")
            for j in data["jobs"]:
                st.write(f"- {j}")

        st.subheader("🚀 What to Learn Next")
        for nxt in data["next"]:
            st.write(f"- {nxt}")

        st.subheader("🧭 Skill Graph")
        fig = generate_skill_graph(skill, data["next"])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🧠 AI Strategic Insights")
        st.write(ai_enhancement(skill))

    else:
        st.warning("Skill not found in database. Try common skills like Python, Web Development, etc.")

st.markdown("---")
st.caption("Built with Streamlit | Designed for practical career intelligence")
