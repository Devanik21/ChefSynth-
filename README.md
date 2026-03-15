# Chefsynth

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/ChefSynth-?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/ChefSynth-?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> AI culinary intelligence — recipe synthesis, flavour pairing science, nutritional analysis, and personalised meal planning powered by generative AI.

---

**Topics:** `content-generation` · `conversational-ai` · `deep-learning` · `food-ai` · `generative-ai` · `knowledge-graph` · `large-language-models` · `neural-networks` · `nlp` · `recipe-generation`

## Overview

ChefSynth is a generative culinary AI platform that applies language models and flavour science to the
full spectrum of cooking assistance: recipe creation from available ingredients, flavour pairing
recommendations grounded in food chemistry, step-by-step cooking guidance with timing coordination,
nutritional breakdown analysis, and personalised weekly meal planning aligned to dietary requirements
and caloric targets.

The recipe synthesis engine takes a list of available ingredients and a set of constraints (cuisine type,
dietary restrictions, cooking time, complexity level, serving size) and generates a complete recipe:
ingredient quantities, equipment list, step-by-step method with timing, plating suggestions, and wine
or beverage pairing. The generation is not random but grounded in culinary principles — flavour balance,
texture contrast, cooking chemistry — through a carefully engineered system prompt that encodes the
knowledge of a trained chef.

The flavour pairing module draws on food chemistry research (notably the FoodPairing.com dataset and
Ahn et al.'s 2011 flavour network study) to suggest ingredient combinations based on shared volatile
aroma compounds. Ingredients that share many aroma compounds tend to taste good together — the
scientific basis behind unexpected but successful pairings like chocolate with blue cheese or
strawberry with black pepper.

---

## Motivation

Home cooking is constrained by two things: knowing what to make with available ingredients, and
understanding the principles that make food taste good. Both are solvable with AI. ChefSynth was
built to be the intelligent kitchen companion that answers 'what can I make with these?' not just
with a recipe but with the culinary reasoning behind it — turning cooking from a lookup activity
into a learning experience.

---

## Architecture

```
User Input: ingredients + constraints
        │
  ┌─────────────────────────────────────────────┐
  │  Recipe Synthesis Engine (LLM)             │
  │  System prompt: culinary principles         │
  │  → Complete recipe with quantities + steps  │
  └─────────────────────────────────────────────┘
        │
  ┌─────────────────────────────────────────────┐
  │  Flavour Pairing Module                    │
  │  Aroma compound graph → pairing suggestions │
  └─────────────────────────────────────────────┘
        │
  Nutritional Analysis (USDA FoodData API)
        │
  Meal Planner (weekly calendar, macro targets)
```

---

## Features

### Ingredient-to-Recipe Synthesis
Input any set of available ingredients plus constraints (cuisine, dietary, time, servings) and receive a complete, coherent recipe with precise quantities, equipment list, and step-by-step method.

### Flavour Pairing Science
Ingredient pairing recommendations grounded in shared volatile aroma compound data — explaining why unexpected combinations work and suggesting novel, scientifically-backed pairings.

### Culinary Technique Guide
Step-by-step technique explanations for any cooking method: emulsification, maillard reaction, tempering chocolate, making roux — with the food science rationale.

### Nutritional Analysis
Per-recipe breakdown of macronutrients (protein, carbohydrates, fat), micronutrients, calories, and dietary suitability (vegan, gluten-free, keto, low-sodium) via USDA FoodData Central API.

### Personalised Meal Planner
7-day meal plan generation aligned to caloric target, macro ratios, dietary restrictions, cuisine preferences, and shopping budget — with a consolidated weekly shopping list.

### Recipe Scaling
Automatically scale any recipe to any serving size with proportionally adjusted ingredient quantities and adapted cooking times.

### Substitution Advisor
For any ingredient in a recipe, suggest scientifically sound substitutes with explanation of how each substitution affects flavour, texture, and cooking behaviour.

### Wine and Beverage Pairing
Contextually appropriate wine, beer, cocktail, or non-alcoholic beverage pairing recommendations with flavour bridge explanations.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **OpenAI GPT-4o / Gemini** | Recipe synthesis | Culinary reasoning, recipe generation, technique explanation |
| **USDA FoodData API** | Nutrition data | Per-ingredient nutritional information |
| **Streamlit** | Application UI | Multi-tab cooking interface |
| **pandas** | Meal planning | Weekly planner grid and shopping list compilation |
| **NetworkX (optional)** | Flavour network | Aroma compound graph for flavour pairing |
| **Plotly** | Nutrition charts | Macro breakdown pie charts, weekly calorie bar charts |

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JavaScript projects)
- A virtual environment manager (`venv`, `conda`, or equivalent)
- API keys as listed in the Configuration section

### Installation

```bash
git clone https://github.com/Devanik21/ChefSynth-.git
cd ChefSynth-
python -m venv venv && source venv/bin/activate
pip install streamlit openai google-generativeai pandas plotly requests python-dotenv
echo 'OPENAI_API_KEY=sk-...' > .env
echo 'USDA_API_KEY=your_usda_key' >> .env
streamlit run app.py
```

---

## Usage

```bash
# Launch app
streamlit run app.py

# Generate recipe from CLI
python generate_recipe.py \
  --ingredients 'chicken, lemon, garlic, rosemary' \
  --cuisine italian --time 30 --servings 4

# Weekly meal plan
python meal_plan.py --calories 2000 --diet vegetarian --days 7

# Analyse nutrition
python nutrition.py --recipe_file recipe.json
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | `(required)` | LLM API key for recipe generation |
| `USDA_API_KEY` | `(optional)` | USDA FoodData Central API key for nutrition data |
| `DEFAULT_SERVINGS` | `4` | Default recipe serving size |
| `DIETARY_RESTRICTIONS` | `none` | Comma-separated restrictions: vegan, gluten-free, keto |
| `CALORIC_TARGET` | `2000` | Daily caloric target for meal planning |

> Copy `.env.example` to `.env` and populate required values before running.

---

## Project Structure

```
ChefSynth/
├── README.md
├── requirements.txt
├── app.py
└── ...
```

---

## Roadmap

- [ ] Computer vision ingredient recognition: identify available ingredients from a fridge photo
- [ ] Recipe rating and personalisation: learn from user ratings to improve future recommendations
- [ ] Integration with grocery delivery APIs (Instacart, AmazonFresh) for direct shopping list fulfilment
- [ ] Video recipe generation: step-by-step instructions formatted for video script production
- [ ] Restaurant menu analyser: paste any menu and receive dish recommendations based on preferences

---

## Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m 'feat: add your idea'`
4. Push to your branch: `git push origin feature/your-idea`
5. Open a Pull Request with a clear description

Please follow conventional commit messages and add documentation for new features.

---

## Notes

Nutritional analysis accuracy depends on USDA FoodData Central data availability for specific ingredients. Custom or exotic ingredients may have limited nutritional data. All recipes are AI-generated — always verify cooking times and internal temperatures for food safety.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with curiosity, depth, and care — because good projects deserve good documentation.*
