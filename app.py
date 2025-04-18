import streamlit as st
import google.generativeai as genai
import json
import os
import random
from datetime import datetime
import pandas as pd
import plotly.express as px


# --- Page Config ---
st.set_page_config(
    page_title="FridgeFeast", 
    layout="wide", 
    page_icon="🍇",
    initial_sidebar_state="expanded"
)

# --- App State Management ---
def init_session_state():
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'recipe_history' not in st.session_state:
        st.session_state.recipe_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            "allergies": [],
            "preferred_cuisines": [],
            "skill_level": "Beginner"
        }

init_session_state()

# --- Theme Switcher ---
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Apply theme
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    :root {
        --background-color: #0e1117;
        --text-color: #f0f2f6;
        --card-bg: #262730;
    }
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .recipe-card {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .recipe-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)



# --- Sidebar ---
with st.sidebar:
    st.title("🍽️ FridgeFeast")
    
    # Theme toggle
    st.button("🌓 Toggle Theme", on_click=toggle_theme)
    
    # API Settings Tab
    with st.expander("🔑 API Settings", expanded=False):
        api_key = st.text_input("Enter your Gemini API Key", type="password")
        st.caption("Your API key is never stored and only used for recipe generation.")
        
    # User Profile
    with st.expander("👤 User Profile", expanded=False):
        st.session_state.user_profile["allergies"] = st.multiselect(
            "Food allergies/restrictions:",
            ["Peanuts", "Tree Nuts", "Dairy", "Eggs", "Seafood", "Gluten", "Soy"],
            st.session_state.user_profile.get("allergies", [])
        )
        
        st.session_state.user_profile["preferred_cuisines"] = st.multiselect(
            "Favorite cuisines:",
            ["Italian", "Chinese", "Indian", "Mexican", "American", "Mediterranean", "Japanese", "Thai", "French"],
            st.session_state.user_profile.get("preferred_cuisines", [])
        )
        
        st.session_state.user_profile["skill_level"] = st.select_slider(
            "Cooking skill level:",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.user_profile.get("skill_level", "Beginner")
        )
    
    # Favorites Expander
    with st.expander("⭐ Saved Recipes", expanded=False):
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{fav['title']}**")
                with col2:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.favorites.pop(i)
                        st.rerun()
            
            # Export favorites
            if st.button("📥 Export Favorites"):
                df = pd.DataFrame(st.session_state.favorites)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    "fridgefeast_favorites.csv",
                    "text/csv",
                    key='download-csv'
                )
        else:
            st.info("Save recipes to see them here!")
    
    # Recipe History
    with st.expander("📜 Recipe History", expanded=False):
        if st.session_state.recipe_history:
            history_df = pd.DataFrame({
                'Date': [h['date'] for h in st.session_state.recipe_history],
                'Ingredients': [h['ingredients'] for h in st.session_state.recipe_history],
                'Count': [len(h.get('recipes', [])) for h in st.session_state.recipe_history]
            })
            st.dataframe(history_df)
            
            # Visualization
            if len(history_df) > 1:
                st.subheader("Your Recipe Journey")
                fig = px.line(history_df, x='Date', y='Count', title='Recipes Generated Over Time')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Generate recipes to see history!")

# --- Main Content Area ---
tab1, tab2, tab3 = st.tabs(["🧑‍🍳 Recipe Generator", "📱 Recipe Browser", "⚙️ Settings"])

with tab1:
    st.markdown("""
    # 🍽️ FridgeFeast  
    #### *Turn your fridge into a feast with AI-generated recipes!*
    """)

    # Camera input for future ingredient detection
    with st.expander("📸 Scan Ingredients (Coming Soon)", expanded=False):
        st.camera_input("Take a picture of your ingredients")
        st.info("AI-powered ingredient detection coming soon! For now, please enter ingredients manually below.")

    # --- Ingredients Input ---
    st.subheader("🥕 What's in your fridge?")
    
    # Enhanced ingredient selection
    ingredient_categories = {
        "Proteins": ["chicken", "beef", "pork", "tofu", "eggs", "beans", "lentils", "chickpeas"],
        "Vegetables": ["tomato", "onion", "spinach", "carrot", "broccoli", "bell pepper", "mushrooms", "zucchini"],
        "Dairy": ["cheese", "milk", "yogurt", "butter", "cream cheese", "heavy cream"],
        "Grains": ["rice", "pasta", "bread", "quinoa", "couscous", "flour", "oats"],
        "Others": ["olive oil", "garlic", "lemon", "soy sauce", "honey", "mayo"]
    }
    
    selected_tab = st.radio("Select by:", ["Categories", "Search"], horizontal=True)
    
    if selected_tab == "Categories":
        selected_ingredients = []
        cols = st.columns(len(ingredient_categories))
        
        for i, (category, items) in enumerate(ingredient_categories.items()):
            with cols[i]:
                st.markdown(f"**{category}**")
                for item in items:
                    if st.checkbox(item, key=f"ing_{item}"):
                        selected_ingredients.append(item)
    else:
        preset_items = sum(ingredient_categories.values(), [])
        selected_ingredients = st.multiselect("Search ingredients:", preset_items)
    
    custom_ingredients = st.text_input("Add any custom ingredients (comma-separated):")
    
    all_ingredients = selected_ingredients + [i.strip() for i in custom_ingredients.split(",") if i.strip()]
    ingredient_str = ", ".join(all_ingredients)
    
    # Display selected ingredients as pills
    if all_ingredients:
        st.write("Selected ingredients:")
        ing_html = "".join([f'<span style="background-color:#e0f7fa;color:#000;padding:3px 8px;margin:2px;border-radius:15px;display:inline-block">{i}</span>' for i in all_ingredients])
        st.markdown(ing_html, unsafe_allow_html=True)

    # --- Ingredient Filter (Disliked) ---
    with st.expander("❌ Ingredients to avoid", expanded=False):
        avoided_ingredients = st.text_input("Enter ingredients to avoid (comma-separated):")
        
        # Auto-include allergies
        if st.session_state.user_profile.get("allergies"):
            st.info(f"Your allergens will be automatically avoided: {', '.join(st.session_state.user_profile['allergies'])}")
    
    avoided_ingredient_list = [i.strip() for i in avoided_ingredients.split(",") if i.strip()] + st.session_state.user_profile.get("allergies", [])
    avoided_ingredient_str = ", ".join(avoided_ingredient_list)

    # --- Preferences ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cuisine_options = ["Any"] + sorted(["Italian", "Chinese", "Indian", "Mexican", "American", "Mediterranean", "Japanese", "Thai", "French", "Greek", "Spanish", "Korean", "Vietnamese", "Middle Eastern"])
        cuisine = st.selectbox("Cuisine", cuisine_options)
        
    with col2:
        meal_type = st.selectbox("Meal type", ["Any", "Main course", "Side dish", "Dessert", "Breakfast", "Snack", "Soup", "Salad", "Appetizer"])
        
    with col3:
        diet = st.selectbox("Dietary preference", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Dairy-Free", "Paleo", "Low-Carb"])
        
    with col4:
        recipe_count = st.slider("Number of recipes", 1, 5, 3)

    # --- Additional Preferences ---
    with st.expander("🔍 Advanced Options", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            cooking_time = st.selectbox("Cooking time", ["Any", "Under 15 minutes", "Under 30 minutes", "Under 1 hour"])
            spice_level = st.slider("Spice level", 1, 5, 2)
            
        with col2:
            skill_required = st.selectbox("Skill level required", ["Any", "Beginner", "Intermediate", "Advanced"])
            calories = st.selectbox("Calories", ["Any", "Low-calorie", "Medium-calorie", "High-calorie"])
    
    # --- Prompt Builder ---
    def build_prompt(ingredients, avoid_ingredients, cuisine, meal_type, diet, count, user_profile, advanced_options=None):
        prompt = f"""
You are a creative and friendly recipe assistant. Create {count} unique, simple, and delicious recipes based on the following ingredients: {ingredients}.

Each recipe MUST include:
- A creative and engaging title
- A short description (2-3 sentences)
- A clear list of ingredients with quantities
- Easy-to-follow instructions (step-by-step)
- Estimated cooking time
- Difficulty level
- Calories estimate (per serving)
- Servings

Present each recipe in a clean, simple markdown format. Use ## headings for recipe titles and single # only for the main sections. Use bullet points for ingredients and numbered lists for instructions.

If specified, avoid using these ingredients: {avoid_ingredients}.
"""
        # Add cuisine preference
        if cuisine != "Any":
            prompt += f"The recipes should follow {cuisine} cuisine.\n"
        elif user_profile.get("preferred_cuisines"):
            prompt += f"Consider these favorite cuisines if relevant: {', '.join(user_profile['preferred_cuisines'])}.\n"
        
        # Add meal type
        if meal_type != "Any":
            prompt += f"The recipes should be suitable for {meal_type.lower()}.\n"
        
        # Add dietary preference
        if diet != "None":
            prompt += f"All recipes must follow a {diet.lower()} diet.\n"
        
        # Advanced options
        if advanced_options:
            if advanced_options.get("cooking_time") and advanced_options["cooking_time"] != "Any":
                prompt += f"Recipes should be prepared {advanced_options['cooking_time'].lower()}.\n"
            
            if advanced_options.get("spice_level"):
                spice_desc = ["very mild", "mild", "medium", "spicy", "very spicy"][advanced_options["spice_level"]-1]
                prompt += f"Spice level should be {spice_desc}.\n"
            
            if advanced_options.get("skill_required") and advanced_options["skill_required"] != "Any":
                prompt += f"Recipes should be appropriate for {advanced_options['skill_required'].lower()} cooks.\n"
            elif user_profile.get("skill_level"):
                prompt += f"Assume the cook has {user_profile['skill_level'].lower()} skill level.\n"
            
            if advanced_options.get("calories") and advanced_options["calories"] != "Any":
                prompt += f"Recipes should be {advanced_options['calories'].lower()}.\n"
        
        prompt += "Separate recipes with a horizontal rule (---). Make the output fun and engaging."
        return prompt

    # Collect advanced options
    advanced_options = {
        "cooking_time": cooking_time,
        "spice_level": spice_level,
        "skill_required": skill_required,
        "calories": calories
    }

    # --- Recipe Generation Actions ---
    col1, col2 = st.columns(2)
    
    with col1:
        generate_button = st.button("🍳 Generate My Recipes", type="primary", use_container_width=True)
    
    with col2:
        surprise_button = st.button("🎲 Surprise Me!", use_container_width=True)

    # Configure API if key provided
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

    # Generate recipes based on inputs
    if generate_button and ingredient_str and api_key:
        prompt = build_prompt(ingredient_str, avoided_ingredient_str, cuisine, meal_type, diet, recipe_count, st.session_state.user_profile, advanced_options)
        
        with st.spinner("Cooking up some recipe magic with Gemini..."):
            try:
                response = model.generate_content(prompt)
                
                # Add to history
                st.session_state.recipe_history.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "ingredients": ingredient_str,
                    "recipes": [{"title": "Recipe"}],  # Simplified for now
                    "response": response.text
                })
                
                st.markdown("## 📖 Your AI-Powered Recipes:")
                
                # Split recipes for individual display and save options
                recipes = response.text.split("---")
                
                for i, recipe in enumerate(recipes):
                    with st.container():
                        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([5, 1])
                        
                        with col1:
                            st.markdown(recipe)
                        
                        with col2:
                            # Extract title from recipe
                            recipe_title = recipe.split('\n')[0].replace('#', '').strip() if recipe else f"Recipe {i+1}"
                            
                            # Save button
                            if st.button("⭐ Save", key=f"save_{i}"):
                                st.session_state.favorites.append({
                                    "title": recipe_title,
                                    "content": recipe,
                                    "ingredients": ingredient_str,
                                    "date_saved": datetime.now().strftime("%Y-%m-%d")
                                })
                                st.success(f"Saved {recipe_title}!")
                            
                            # Share button (placeholder)
                            if st.button("📤 Share", key=f"share_{i}"):
                                st.info("Sharing will be available soon!")
                                
                            # Print button
                            if st.button("🖨️ Print", key=f"print_{i}"):
                                st.info("Print-friendly version coming soon!")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    # Random recipe generation
    elif surprise_button and api_key:
        # Randomize parameters
        random_categories = random.sample(list(ingredient_categories.keys()), k=2)
        random_ingredients = []
        
        for category in random_categories:
            random_ingredients.extend(random.sample(ingredient_categories[category], k=min(3, len(ingredient_categories[category]))))
        
        random_ingredient_str = ", ".join(random_ingredients)
        
        random_cuisine = random.choice(["Any"] + st.session_state.user_profile.get("preferred_cuisines", []))
        random_meal = random.choice(["Main course", "Side dish", "Dessert", "Breakfast"])
        
        st.info(f"Surprising you with: {random_ingredient_str} ({random_cuisine}, {random_meal})")
        
        prompt = build_prompt(random_ingredient_str, avoided_ingredient_str, random_cuisine, random_meal, diet, 1, st.session_state.user_profile)
        
        with st.spinner("Creating a surprising recipe with Gemini..."):
            try:
                response = model.generate_content(prompt)
                
                st.markdown("## 🎉 Your Surprise Recipe:")
                
                with st.container():
                    st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        st.markdown(response.text)
                    
                    with col2:
                        # Extract title
                        recipe_title = response.text.split('\n')[0].replace('#', '').strip() if response.text else "Surprise Recipe"
                        
                        # Save button
                        if st.button("⭐ Save", key="save_surprise"):
                            st.session_state.favorites.append({
                                "title": recipe_title,
                                "content": response.text,
                                "ingredients": random_ingredient_str,
                                "date_saved": datetime.now().strftime("%Y-%m-%d")
                            })
                            st.success(f"Saved {recipe_title}!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    elif not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
    elif not ingredient_str and (generate_button or surprise_button):
        st.info("Add some ingredients to start generating recipes!")

# --- Recipe Browser Tab ---
with tab2:
    st.header("📱 Recipe Browser")
    
    if not st.session_state.favorites:
        st.info("You haven't saved any recipes yet. Generate and save recipes to see them here!")
    else:
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            search_term = st.text_input("🔍 Search saved recipes", "")
        with filter_col2:
            sort_by = st.selectbox("Sort by:", ["Latest", "Oldest", "A-Z"])
        
        # Apply filters and sorting
        filtered_recipes = st.session_state.favorites
        
        if search_term:
            filtered_recipes = [r for r in filtered_recipes if search_term.lower() in r['title'].lower() or search_term.lower() in r.get('ingredients', '').lower()]
        
        if sort_by == "Latest":
            filtered_recipes = sorted(filtered_recipes, key=lambda x: x.get('date_saved', ''), reverse=True)
        elif sort_by == "Oldest":
            filtered_recipes = sorted(filtered_recipes, key=lambda x: x.get('date_saved', ''))
        elif sort_by == "A-Z":
            filtered_recipes = sorted(filtered_recipes, key=lambda x: x['title'])
        
        # Display recipes in grid
        if filtered_recipes:
            recipe_cols = st.columns(3)
            for i, recipe in enumerate(filtered_recipes):
                with recipe_cols[i % 3]:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd;border-radius:10px;padding:15px;margin-bottom:15px;height:200px;overflow:hidden;">
                        <h3>{recipe['title']}</h3>
                        <p><small>Saved on: {recipe.get('date_saved', 'Unknown')}</small></p>
                        <p><small>Ingredients: {recipe.get('ingredients', 'Various')[:50]}...</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("View", key=f"view_{i}"):
                            st.session_state.selected_recipe = recipe
                            st.rerun()
                    with col2:
                        if st.button("Delete", key=f"delete_browse_{i}"):
                            st.session_state.favorites.remove(recipe)
                            st.rerun()
        else:
            st.warning("No recipes match your search criteria.")
    
    # Recipe detail view
    if 'selected_recipe' in st.session_state and st.session_state.selected_recipe:
        recipe = st.session_state.selected_recipe
        
        with st.expander("Recipe Details", expanded=True):
            st.markdown(recipe['content'])
            
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button("← Back to List"):
                    del st.session_state.selected_recipe
                    st.rerun()
            with col2:
                if st.button("🖨️ Print Recipe"):
                    st.info("Print functionality coming soon!")
            with col3:
                if st.button("📤 Share Recipe"):
                    st.info("Sharing functionality coming soon!")

# --- Settings Tab ---
with tab3:
    st.header("⚙️ Settings")
    
    st.subheader("Application Settings")
    
    # Data management
    with st.expander("Data Management"):
        st.write("Manage your saved recipes and application data")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export All Data", use_container_width=True):
                export_data = {
                    "favorites": st.session_state.favorites,
                    "recipe_history": st.session_state.recipe_history,
                    "user_profile": st.session_state.user_profile
                }
                
                export_json = json.dumps(export_data)
                st.download_button(
                    "📥 Download JSON",
                    export_json,
                    "fridgefeast_data.json",
                    "application/json",
                    key='download-json'
                )
        
        with col2:
            if st.button("Clear All Data", use_container_width=True):
                st.warning("This will delete all your saved recipes and history. This action cannot be undone!")
                confirm = st.checkbox("I understand, clear my data")
                
                if confirm and st.button("Confirm Clear Data"):
                    st.session_state.favorites = []
                    st.session_state.recipe_history = []
                    st.success("All data cleared!")
    
    # Import functionality
    with st.expander("Import Data"):
        st.write("Import previously exported data")
        uploaded_file = st.file_uploader("Upload JSON data file", type=['json'])
        
        if uploaded_file is not None:
            try:
                import_data = json.loads(uploaded_file.getvalue().decode("utf-8"))
                
                if st.button("Import Data"):
                    if "favorites" in import_data:
                        st.session_state.favorites = import_data["favorites"]
                    if "recipe_history" in import_data:
                        st.session_state.recipe_history = import_data["recipe_history"]
                    if "user_profile" in import_data:
                        st.session_state.user_profile = import_data["user_profile"]
                    
                    st.success("Data imported successfully!")
            except Exception as e:
                st.error(f"Error importing data: {e}")
    
    # App information
    st.subheader("About FridgeFeast")
    st.write("""
    FridgeFeast is an AI-powered recipe generator that helps you create delicious meals from ingredients you already have.
    
    **Version:** 2.0
    **Created with:** Streamlit and Google Gemini AI
    
    For support or feedback, please contact support@fridgefeast.example.com
    """)

# --- Footer ---
st.markdown("""
---
<div style="text-align:center">
    <p>© 2025 FridgeFeast | Made with ❤️ and Streamlit | Powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)
