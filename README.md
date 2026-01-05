## 🔗 Live Demo

👉   https://talk-to-data-6nycmyj85ukhi86ncjpgzd.streamlit.app/

# 📊 SQL Data Analyst Assistant — Talk to Data

An LLM-powered analytics assistant that allows users to explore relational data using natural language instead of SQL.

The application converts user questions into safe, read-only SQL queries, executes them on a SQLite database, and returns structured results with optional visualizations.

---

## 🚀 Features

- Natural language → SQL query generation
- Read-only SQL enforcement (SELECT-only)
- Automatic database initialization (auto-bootstrap)
- Data preview to help users understand available data
- Interactive Streamlit UI
- Optional data visualizations

---

## 🧠 How It Works

1. On startup, the app checks whether the database and table exist
2. If not, it automatically creates and seeds the database
3. The user asks a question in natural language
4. An LLM generates a safe SQL query
5. The query is validated and executed
6. Results are displayed as a table and (optionally) a chart

---

## 📂 Dataset

The database contains tourism statistics with the following schema:
tourism_stats(
country TEXT,
year INTEGER,
visitors_millions REAL,
tourism_revenue_usd REAL
)

A data preview is shown at the top of the app to help users understand what can be queried.

---

## ❓ Example Questions

### Basic Queries

- Which country had the highest tourism revenue in 2023?
- Show visitors by country for 2023
- List all countries and their tourism revenue

### Comparisons & Rankings

- Compare tourism revenue across countries in 2023
- Rank countries by number of visitors
- Show top 3 countries by visitors

### Time-Series Analysis

- How did tourism revenue change over time for Japan?
- Compare visitors in 2019 and 2023
- Show tourism trends for each country

### Aggregations

- What is the total number of visitors by year?
- What is the average tourism revenue per country?
- Which country had the biggest recovery after 2022?

### Edge Cases (Handled Gracefully)

- Show tourism revenue for Mars
- Delete all data from the table

---

## 🛡️ Safety & Reliability

- Only SELECT queries are allowed
- LLM-generated SQL is sanitized before execution
- Retry logic prevents infinite loops
- Invalid or unsafe queries fail gracefully

---

## 🧰 Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- OpenAI (via LangChain)

---

## ▶️ Running the App

```bash
pip install -r requirements.txt
setx OPENAI_API_KEY "your_api_key_here"
streamlit run app.py

Open your browser at:
http://localhost:8501

📌 Project Goal

Enable non-technical users to explore and analyze structured data using natural language, without needing SQL knowledge.




```
