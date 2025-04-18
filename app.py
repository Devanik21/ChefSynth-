import streamlit as st
import google.generativeai as genai

# --- Sidebar for API Key ---
st.sidebar.title("🔑 API Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# --- Set up Gemini ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

# --- App Header ---
st.set_page_config(page_title="FridgeFeast 🍽️", layout="wide")
st.title("FridgeFeast 🍽️")
st.write("Generate simple, tasty recipes based on what you have in the fridge.")

# --- Inputs ---
ingredients = st.text_input("Your ingredients (comma-separated)", placeholder="e.g., tomato, cheese, onion")

col1, col2 = st.columns(2)
with col1:
    cuisine = st.selectbox("Preferred cuisine", ["", "Italian", "Chinese", "Indian", "Mexican", "American"])
with col2:
    meal_type = st.selectbox("Meal type", ["", "main course", "side dish", "dessert", "breakfast", "snack", "soup"])

num_recipes = st.slider("How many recipe ideas?", 1, 5, 3)

# --- Prompt Construction ---
def build_prompt(ingredients, cuisine, meal_type, count):
    prompt = f"""
You are a helpful recipe assistant. Suggest {count} unique, simple recipes using the following ingredients: {ingredients}.
Each recipe should include:
- A title
- A short description
- A list of ingredients
- Step-by-step instructions

"""
    if cuisine:
        prompt += f"The recipes should follow {cuisine} cuisine.\n"
    if meal_type:
        prompt += f"These should be suitable for {meal_type}.\n"

    prompt += "Present each recipe in a clean format."
    return prompt

# --- Recipe Generation ---
if st.button("Generate Recipes 🍳") and ingredients and api_key:
    prompt = build_prompt(ingredients, cuisine, meal_type, num_recipes)

    with st.spinner("Cooking up something delicious with Gemini..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif not api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")

