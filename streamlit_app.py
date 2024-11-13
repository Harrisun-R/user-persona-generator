# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
import random

# Set up the Streamlit app
st.title("User Persona Generator")
st.write(f"Developed by Harrisun Raj Mohan")
st.write(f"[Connect on LinkedIn](https://www.linkedin.com/in/harrisun-raj-mohan/)")
st.write("Create detailed user personas based on input information. Align product strategies with target audiences effectively.")

# Step 1: User Inputs for Persona Details
st.header("User Persona Details")

# Persona Template Suggestions
persona_templates = ["Tech-Savvy Millennial", "Working Parent", "Senior Citizen", "Frequent Traveler", "Fitness Enthusiast"]
persona_template = st.selectbox("Choose a Persona Template", persona_templates)

# Input fields for Demographics
st.subheader("Demographics")
age = st.slider("Age", 18, 65, 30)
gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary", "Other"])
location = st.text_input("Location", "New York")
occupation = st.text_input("Occupation", "Software Engineer")

# Behavioral Inputs
st.subheader("Behaviors")
interests = st.text_area("List Interests (separate by commas)", "e.g., technology, fitness, travel")
frequency = st.selectbox("Frequency of Product Use", ["Daily", "Weekly", "Monthly", "Rarely"])

# Needs and Pain Points
st.subheader("Needs and Pain Points")
needs = st.text_area("What are their primary needs?", "e.g., convenience, efficiency, affordability")
pain_points = st.text_area("What are their pain points?", "e.g., lack of time, high cost, complexity")

# Step 2: Generate Persona Summary
st.header("Generated Persona Summary")

# Creating a DataFrame to display persona details
persona_data = {
    "Category": ["Age", "Gender", "Location", "Occupation", "Interests", "Frequency of Product Use", "Needs", "Pain Points", "Persona Template"],
    "Details": [age, gender, location, occupation, interests, frequency, needs, pain_points, persona_template]
}

persona_df = pd.DataFrame(persona_data)

# Displaying the DataFrame
st.write("### Persona Overview")
st.dataframe(persona_df)

# Step 3: Persona Comparison
# If there are multiple personas generated, compare them here
persona_comparison = st.checkbox("Enable Persona Comparison")

if persona_comparison:
    st.write("### Persona Comparison")
    # Allow users to input details for multiple personas
    personas = []
    for i in range(2):
        st.write(f"**Persona {i+1}:**")
        persona_data_comparison = {
            "Category": ["Age", "Gender", "Location", "Occupation", "Interests", "Frequency of Product Use", "Needs", "Pain Points"],
            "Details": [st.slider(f"Age for Persona {i+1}", 18, 65, 30),
                        st.selectbox(f"Gender for Persona {i+1}", ["Male", "Female", "Non-Binary", "Other"]),
                        st.text_input(f"Location for Persona {i+1}", "New York"),
                        st.text_input(f"Occupation for Persona {i+1}", "Software Engineer"),
                        st.text_area(f"List Interests for Persona {i+1}", "e.g., technology, fitness, travel"),
                        st.selectbox(f"Frequency of Product Use for Persona {i+1}", ["Daily", "Weekly", "Monthly", "Rarely"]),
                        st.text_area(f"What are their primary needs for Persona {i+1}?", "e.g., convenience, efficiency, affordability"),
                        st.text_area(f"What are their pain points for Persona {i+1}?", "e.g., lack of time, high cost, complexity")]
        }
        personas.append(pd.DataFrame(persona_data_comparison))
    st.write(pd.concat(personas))

# Step 4: Persona Scoring
st.header("Persona Scoring")
persona_score = st.slider("Score the Persona on Likelihood to Convert", 1, 10, 7)
st.write(f"Persona Score: {persona_score}/10")

# Step 5: Visualization of Needs and Pain Points
st.header("Needs and Pain Points Visualization")
needs_pain_points = {"Needs": needs, "Pain Points": pain_points}
needs_pain_points_df = pd.DataFrame(list(needs_pain_points.items()), columns=["Category", "Details"])

fig = px.bar(needs_pain_points_df, x="Category", y="Details", title="Needs and Pain Points")
st.plotly_chart(fig)

# Step 6: Demographic Heatmap
st.header("Demographic Heatmap")
age_distribution = [random.randint(18, 65) for _ in range(100)]
location_distribution = random.choices(["New York", "Los Angeles", "Chicago", "San Francisco"], k=100)
age_df = pd.DataFrame({"Age": age_distribution, "Location": location_distribution})

age_heatmap = px.density_mapbox(age_df, lat="Age", lon="Location", z="Age", radius=10,
                                mapbox_style="open-street-map", title="Demographic Heatmap")
st.plotly_chart(age_heatmap)

# Step 7: Export Persona as PDF
st.header("Export Persona as PDF")
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="User Persona Details", ln=True, align="C")
for index, row in persona_df.iterrows():
    pdf.cell(200, 10, txt=f"{row['Category']}: {row['Details']}", ln=True, align="L")

# Convert PDF to bytes and provide download link
pdf_bytes = BytesIO()
pdf.output(pdf_bytes)
pdf_bytes.seek(0)

st.download_button("Download Persona as PDF", pdf_bytes, file_name="user_persona.pdf", mime="application/pdf")

# Step 8: Real-Time Collaboration
st.header("Real-Time Collaboration (Work-in-progress)")
st.write("Share this link with others to collaborate on building the persona in real-time.")

# Step 9: Dynamic Trait Generation Based on Inputs
st.header("Dynamic Trait Generation")
if "tech-savvy" in interests.lower():
    st.write("This persona is likely to prefer cutting-edge technology, apps, and devices.")
if "fitness" in interests.lower():
    st.write("This persona values health and fitness, prefers products related to exercise and well-being.")
    
# Step 10: Thank You Message
st.write("Thank you for using the User Persona Generator!")