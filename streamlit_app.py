# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
import random
import json

# Set up the Streamlit app
st.title("User Persona Generator")
st.write(f"Developed by Harrisun Raj Mohan")
st.write(f"[Connect on LinkedIn](https://www.linkedin.com/in/harrisun-raj-mohan/)")
st.write("Create detailed user personas based on input information. Align product strategies with target audiences effectively.")

personas = []

# Step 1: Input persona details
st.header("Create User Personas")
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

# Display all personas
if personas:
    st.header("Created Personas")
    personas_df = pd.DataFrame(personas)
    st.write(personas_df)

    # Step 2: Export personas as JSON
    st.subheader("Export Personas as JSON")
    personas_json = json.dumps(personas, indent=4)
    st.download_button(
        label="Download Personas as JSON",
        data=personas_json,
        file_name="personas.json",
        mime="application/json"
    )

# Step 3: Import personas from JSON
st.subheader("Import Personas from JSON")
uploaded_file = st.file_uploader("Upload a JSON file with personas", type="json")
if uploaded_file:
    imported_personas = json.load(uploaded_file)
    st.success("Personas imported successfully!")
    st.write(imported_personas)

    # Merge imported personas with the current ones
    personas.extend(imported_personas)
    personas_df = pd.DataFrame(personas)
    st.write(personas_df)

# Step 4: Export personas as PDF
if personas:
    st.header("Export Personas as PDF")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="User Persona Details", ln=True, align="C")

    for persona in personas:
        pdf.cell(0, 10, txt=f"Name: {persona['Name']}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Age: {persona['Age']}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Location: {persona['Location']}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Behavior: {persona['Behavior']}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Needs: {persona['Needs']}", ln=True, align="L")
        pdf.cell(0, 10, txt=f"Pain Points: {persona['Pain Points']}", ln=True, align="L")
        pdf.cell(0, 10, txt="", ln=True, align="L")  # Blank line between personas

    # Save PDF and provide download link
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
    
# Step 10: Thank You Message
st.write("Thank you for using the User Persona Generator!")
