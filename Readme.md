🌍⚖️ Nutrition Paradox: Obesity vs Malnutrition 🍔🥦
A Streamlit-based web app that visualizes the global nutrition imbalance—rising obesity levels alongside persistent malnutrition. Use SQL-powered insights to explore trends, disparities, and regional health statistics across the world.

🧠 Features
🔎 Filter & Query by Data Category
Choose between:

Obesity Data

Malnutrition Data

Combined Comparison

Each category provides 10+ pre-built SQL insights rendered as interactive tables.

📊 Insightful SQL Queries
Get answers to health trends like:

🌍 Top 5 regions with highest obesity (2022)

📉 Countries with decreasing malnutrition

👩‍⚖️ Gender-based disparities in both domains

🧒 Age-wise nutrition trends

⚠️ Reliability indicators using CI width

🎯 Streamlit UI Navigation
Smooth dropdown filters and query selectors

Responsive, auto-updating tables

Organized by category (Obesity / Malnutrition / Combined)

📁 Project Structure
bash
Copy
Edit
📦 nutrition-paradox
├── Nutrition_paradox_streamlit.py     # Main Streamlit dashboard
├── requirements.txt                   # Required Python libraries
└── README.md                          # You’re reading it!
⚙️ How to Run
🐍 Step 1: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
📂 Step 2: Clone the Repository
bash
Copy
Edit
git clone https://github.com/YuvanVarshith/nutrition-paradox.git
cd nutrition-paradox
▶️ Step 3: Launch the App
bash
Copy
Edit
streamlit run Nutrition_paradox_streamlit.py
Then open http://localhost:8501 in your browser.

🧮 Data Source
SQL database (nutrition_paradox)

Two main tables: obesity and malnutrition

Data includes: region, country, year, gender, age group, mean estimates, confidence intervals

📚 Sample SQL Insights
Obesity trend in India over the years

Countries with consistent low obesity

Countries where female obesity > male

High CI_Width malnutrition flags

Countries with obesity up & malnutrition down

Region-wise average comparisons (Africa vs America)

💡 Future Enhancements
📈 Add visual plots (bar, pie, line)

📌 Add real-time input filters (sliders, multiselect)

🌐 Deploy to cloud (Streamlit Share / HuggingFace / Render)

🙌 Acknowledgments
Thanks to global health open datasets for providing obesity & malnutrition statistics.

Inspired by real-world public health challenges and the power of SQL + Streamlit for storytelling.

