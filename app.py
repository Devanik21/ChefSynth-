import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from fpdf import FPDF
from io import BytesIO
import os
import base64

# --- Page Config (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="FridgeFeast", layout="wide", page_icon="🍇")

# --- Custom CSS ---
st.markdown("""
    <style>
        .block-container {padding: 2rem;}
        .recipe-box {
            background-color: rgba(255,255,255,0.05);
            padding: 1.2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🔑 API Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# --- Configure Gemini ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

# --- Header ---
st.title("🍽️ FridgeFeast")
st.write("Turn your ingredients into delicious meals using Gemini AI!")

# --- Input Section ---
st.markdown("#### 🛒 Your Ingredients")

# Option to use speech
use_voice = st.checkbox("🎙️ Use voice input instead of typing")

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎤 Listening... Speak your ingredients clearly.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Speech recognition error: {e}")
    return ""

if use_voice:
    if st.button("Start Recording"):
        ingredients = recognize_speech()
    else:
        ingredients = ""
else:
    ingredients = st.text_input("List ingredients (comma-separated)", placeholder="e.g., tomato, cheese, onion")

col1, col2, col3 = st.columns(3)
with col1:
    cuisine = st.selectbox("🌎 Cuisine", ["", "Italian", "Chinese", "Indian", "Mexican", "American"])
with col2:
    meal_type = st.selectbox("🍱 Meal Type", ["", "main course", "side dish", "dessert", "breakfast", "snack", "soup"])
with col3:
    num_recipes = st.slider("📋 Number of Recipes", 1, 5, 3)

# --- Prompt Construction ---
def build_prompt(ingredients, cuisine, meal_type, count):
    prompt = f"""
You are a helpful recipe assistant. Suggest {count} unique, simple recipes using these ingredients: {ingredients}.
Each recipe must include:
- A title
- A short description
- A list of ingredients
- Step-by-step instructions
"""
    if cuisine:
        prompt += f"The recipes should follow {cuisine} cuisine.\n"
    if meal_type:
        prompt += f"These should be suitable for {meal_type}.\n"

    prompt += "Present each recipe in clean markdown formatting with line breaks between recipes."
    return prompt

# --- PDF Export ---
def generate_pdf(recipes_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in recipes_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer

# --- Generate Recipes ---
if st.button("🍳 Generate Recipes") and ingredients and api_key:
    prompt = build_prompt(ingredients, cuisine, meal_type, num_recipes)

    with st.spinner("👩‍🍳 Gemini is preparing your recipes..."):
        try:
            response = model.generate_content(prompt)
            recipes = response.text

            for r in recipes.split("\n\n"):
                st.markdown(f"<div class='recipe-box'>{st.markdown(r)}</div>", unsafe_allow_html=True)

            # Download as PDF
            pdf_bytes = generate_pdf(recipes)
            b64_pdf = base64.b64encode(pdf_bytes.getvalue()).decode()
            st.download_button("📥 Download Recipes as PDF", data=pdf_bytes, file_name="fridgefeast_recipes.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

elif not api_key:
    st.warning("🔐 Please enter your Gemini API key in the sidebar to begin.")
