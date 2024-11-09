# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit app
st.title("User Persona Generator")
st.write(f"Developed by Harrisun Raj Mohan")
st.write(f"[Connect on LinkedIn](https://www.linkedin.com/in/harrisun-raj-mohan/)")
st.write("Create detailed user personas based on input information. Align product strategies with target audiences effectively.")

# Step 1: User Inputs for Persona Details
st.header("User Persona Details")

# Demographic inputs
st.subheader("Demographics")
age = st.slider("Age", 18, 65, 30)
gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary", "Other"])
location = st.text_input("Location")
occupation = st.text_input("Occupation")

# Behavioral inputs
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
    "Category": ["Age", "Gender", "Location", "Occupation", "Interests", "Frequency of Product Use", "Needs", "Pain Points"],
    "Details": [age, gender, location, occupation, interests, frequency, needs, pain_points]
}

persona_df = pd.DataFrame(persona_data)

# Displaying the DataFrame
st.write("### Persona Overview")
st.dataframe(persona_df)

# Step 3: Visualize Persona Traits
st.header("Persona Traits Visualization")

# Count of Interests Visualization
interests_list = [interest.strip() for interest in interests.split(",")]
interest_counts = pd.DataFrame(interests_list, columns=["Interest"])
interest_counts['Count'] = 1

# Plotting interests using Plotly
if not interest_counts.empty:
    fig = px.bar(interest_counts, x="Interest", y="Count", title="Interests of the Persona", labels={"Count": "Frequency"})
    st.plotly_chart(fig)

st.write("### Summary")
st.write(f"This persona is a {age}-year-old {gender} based in {location} working as a {occupation}. They typically use the product {frequency.lower()} and are interested in {interests.lower()}. Their main needs include {needs.lower()}, while they struggle with {pain_points.lower()}.")

st.write("Thank you for using the User Persona Generator!")
