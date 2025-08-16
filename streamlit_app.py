# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import requests
import json

# --------------------------
# 🔑 API Configuration
# --------------------------
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-oss-20b:free"

def generate_persona_with_ai(prompt):
    def generate_persona_with_ai(prompt):
    """Generate a user persona using OpenRouter AI."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site-url.com",  # Optional
        "X-Title": "User Persona Generator App",       # Optional
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert product researcher."},
            {
                "role": "user",
                "content": f"""
Generate a user persona for: {prompt}.

Return ONLY valid JSON with fields:
Name (string), Age (int), Location (string), Behavior (string), Needs (string), Pain Points (string).
No explanations, no extra text, just JSON.
"""
            }
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        try:
            result = response.json()
            ai_text = result["choices"][0]["message"]["content"].strip()

            # 🛠 Ensure we extract JSON only (in case AI wraps it in text)
            if ai_text.startswith("```"):
                ai_text = ai_text.strip("```json").strip("```").strip()

            persona = json.loads(ai_text)  # Parse into dict
            return persona

        except Exception as e:
            st.error(f"Error parsing AI response: {e}")
            st.write("🔍 Raw AI Response:", ai_text)  # Debug output
            return None
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return None

# --------------------------
# Streamlit UI
# --------------------------
st.title("🤖 User Persona Generator (Enhanced with AI)")
st.write("Developed by Harrisun Raj Mohan")
st.write("[Connect on LinkedIn](https://www.linkedin.com/in/harrisun-raj-mohan/)")
st.write("Create detailed user personas manually or with AI assistance.")

personas = []

# Step 1: Manual Input
st.header("📌 Create User Personas Manually")
num_personas = st.number_input("Number of personas to create", min_value=1, max_value=10, value=1, step=1)

for i in range(num_personas):
    st.subheader(f"Persona {i + 1}")
    name = st.text_input(f"Name for Persona {i + 1}")
    age = st.number_input(f"Age for Persona {i + 1}", min_value=0, max_value=120, value=25)
    location = st.text_input(f"Location for Persona {i + 1}")
    behavior = st.text_area(f"Behavior for Persona {i + 1}")
    needs = st.text_area(f"Needs for Persona {i + 1}")
    pain_points = st.text_area(f"Pain Points for Persona {i + 1}")

    if st.button(f"Add Persona {i + 1}"):
        personas.append({
            "Name": name,
            "Age": age,
            "Location": location,
            "Behavior": behavior,
            "Needs": needs,
            "Pain Points": pain_points
        })
        st.success(f"Persona {i + 1} added successfully!")

# Step 2: AI Persona Generator
st.header("✨ Generate Personas with AI")
ai_prompt = st.text_area("Describe the target audience or context (e.g., 'college students in Bangalore who use fintech apps')")

if st.button("Generate Persona with AI"):
    if ai_prompt.strip():
        ai_persona = generate_persona_with_ai(ai_prompt)
        if ai_persona:
            personas.append(ai_persona)
            st.success("AI Persona generated and added successfully!")
            st.json(ai_persona)
    else:
        st.warning("Please enter a description for the AI to generate a persona.")

# Step 3: Display Personas
if personas:
    st.header("👥 Created Personas")
    personas_df = pd.DataFrame(personas)
    st.write(personas_df)

    # Export JSON
    st.subheader("📤 Export Personas as JSON")
    personas_json = json.dumps(personas, indent=4)
    st.download_button(
        label="Download Personas as JSON",
        data=personas_json,
        file_name="personas.json",
        mime="application/json"
    )

# Step 4: Import JSON
st.subheader("📥 Import Personas from JSON")
uploaded_file = st.file_uploader("Upload a JSON file with personas", type="json")
if uploaded_file:
    imported_personas = json.load(uploaded_file)
    st.success("Personas imported successfully!")
    st.write(imported_personas)
    personas.extend(imported_personas)

# Step 5: Export PDF
if personas:
    st.header("📑 Export Personas as PDF")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="User Persona Details", ln=True, align="C")

    for persona in personas:
        pdf.cell(0, 10, txt=f"Name: {persona.get('Name', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Age: {persona.get('Age', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Location: {persona.get('Location', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Behavior: {persona.get('Behavior', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Needs: {persona.get('Needs', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Pain Points: {persona.get('Pain Points', '')}", ln=True, align="L")
        pdf.cell(0, 10, txt="", ln=True, align="L")

    temp_file = "temp_personas.pdf"
    pdf.output(temp_file)
    with open(temp_file, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="Download Personas as PDF",
        data=pdf_bytes,
        file_name="user_personas.pdf",
        mime="application/pdf"
    )

# Footer
st.write("✅ Thank you for using the AI-powered User Persona Generator!")
