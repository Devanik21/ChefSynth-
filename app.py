import streamlit as st
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(page_title="FridgeFeast", layout="wide", page_icon="🍇")

# --- Sidebar ---
st.sidebar.title("🔑 Gemini API Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

# --- App Header ---
st.markdown("""
# 🍽️ FridgeFeast  
#### *Turn your fridge into a feast with AI-generated recipes!*
""")

st.markdown("🧑‍🍳 **Just tell us what's in your fridge, and we'll whip up some tasty ideas.**")

# --- Ingredients Input ---
st.subheader("🥕 What's in your fridge?")
preset_items = ["tomato", "cheese", "onion", "spinach", "chicken", "eggs", "rice", "milk", "bread", "mushrooms"]
selected_ingredients = st.multiselect("Select from common ingredients:", preset_items)
custom_ingredients = st.text_input("Add any custom ingredients (comma-separated):")

all_ingredients = selected_ingredients + [i.strip() for i in custom_ingredients.split(",") if i.strip()]
ingredient_str = ", ".join(all_ingredients)

# --- Preferences ---
st.subheader("🎯 Preferences")

col1, col2, col3 = st.columns(3)

with col1:
    cuisine = st.selectbox("Preferred cuisine", ["Any", "Italian", "Chinese", "Indian", "Mexican", "American", "Mediterranean"])

with col2:
    meal_type = st.selectbox("Meal type", ["Any", "Main course", "Side dish", "Dessert", "Breakfast", "Snack", "Soup"])

with col3:
    diet = st.selectbox("Dietary preference", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Dairy-Free"])

num_recipes = st.slider("How many recipes do you want?", 1, 5, 3)

# --- Prompt Builder ---
def build_prompt(ingredients, cuisine, meal_type, diet, count):
    prompt = f"""
You are a creative and friendly recipe assistant. Create {count} unique, simple, and delicious recipes based on the following ingredients: {ingredients}.
Each recipe must include:
- A creative title
- A short description
- A clear list of ingredients
- Easy-to-follow instructions (step-by-step)

Respond in clean markdown format with each recipe in a collapsible section using headings.

"""
    if cuisine != "Any":
        prompt += f"The recipes should follow {cuisine} cuisine.\n"
    if meal_type != "Any":
        prompt += f"They should be suitable for {meal_type.lower()}.\n"
    if diet != "None":
        prompt += f"All recipes must follow a {diet.lower()} diet.\n"

    prompt += "Avoid repeating ingredients unnecessarily. Make the output fun and engaging."
    return prompt

# --- Generate Recipes ---
if st.button("🍳 Generate My Recipes") and ingredient_str and api_key:
    prompt = build_prompt(ingredient_str, cuisine, meal_type, diet, num_recipes)

    with st.spinner("Cooking up some recipe magic with Gemini..."):
        try:
            response = model.generate_content(prompt)
            st.markdown("## 📖 Your AI-Powered Recipes:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif not api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")
elif not ingredient_str:
    st.info("Add some ingredients to start generating recipes!")
