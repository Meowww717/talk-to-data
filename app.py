import os
import sqlite3
import pandas as pd
import streamlit as st
from typing import Optional

from langchain_openai import ChatOpenAI
from db_setup import setup_database

# CONFIG
DB_PATH = "data.db"
MODEL_NAME = "gpt-4o-mini"
MAX_ATTEMPTS = 2


def table_exists(table_name: str) -> bool:
    if not os.path.exists(DB_PATH):
        return False

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        return cur.fetchone() is not None
    finally:
        conn.close()


if not table_exists("tourism_stats"):
    setup_database()

# LLM
llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

# DATABASE


def get_connection():
    return sqlite3.connect(DB_PATH)

# SQL GENERATION


def generate_sql(question: str, error: Optional[str] = None) -> str:
    error_context = f"\nPrevious error: {error}" if error else ""

    prompt = f"""
You are a senior data analyst.

Generate a READ-ONLY SQLite SQL query for the table:

tourism_stats(
    country TEXT,
    year INTEGER,
    visitors_millions REAL,
    tourism_revenue_usd REAL
)

Rules:
- ONLY SELECT statements
- NO INSERT, UPDATE, DELETE
- Return ONLY raw SQL
- Do NOT use markdown
- Do NOT add explanations or comments
- The response MUST start with SELECT
- Use valid SQLite syntax

Question:
{question}
{error_context}
"""

    raw = llm.invoke(prompt).content.strip()

    # -------- SQL SANITIZER --------
    sql = raw.replace("```sql", "").replace("```", "").strip()

    # cut everything before the first SELECT
    lower_sql = sql.lower()
    if "select" in lower_sql:
        sql = sql[lower_sql.find("select"):]

    # SAFETY GUARD
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    return sql

# SQL EXECUTION


def execute_sql(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql(sql, conn)
    finally:
        conn.close()


def load_table_preview(limit: int = 10) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql(
            f"SELECT * FROM tourism_stats LIMIT {limit}", conn
        )
    finally:
        conn.close()

# PIPELINE


def run_text_to_sql(question: str, max_attempts: int = MAX_ATTEMPTS):
    attempts = 0
    last_error = None

    while attempts <= max_attempts:
        try:
            sql = generate_sql(question, last_error)
            df = execute_sql(sql)
            return {
                "sql": sql,
                "result": df,
                "error": None,
                "attempts": attempts,
            }
        except Exception as e:
            last_error = str(e)
            attempts += 1

    return {
        "sql": None,
        "result": None,
        "error": last_error,
        "attempts": attempts,
    }


# STREAMLIT UI
st.set_page_config(page_title="Talk to Data", layout="wide")

st.title("📊 SQL Data Analyst Assistant — Talk to Data")
st.caption(
    "Ask questions in natural language. SQL is generated and executed automatically."
)

with st.expander("📄 View available data (table preview)", expanded=True):
    preview_df = load_table_preview(limit=10)
    st.dataframe(preview_df, use_container_width=True)

    st.markdown(
        """
        **Available columns:**
        - `country` — Country name  
        - `year` — Year  
        - `visitors_millions` — Number of visitors (in millions)  
        - `tourism_revenue_usd` — Tourism revenue (USD, billions)
        """
    )

question = st.text_input("Ask a question about the data:")

if question:
    with st.spinner("Analyzing..."):
        result = run_text_to_sql(question)

    if result["error"]:
        st.error("❌ Could not generate a valid SQL query.")
        st.code(result["error"])
    else:
        st.success("✅ Query executed successfully")

        st.subheader("Generated SQL")
        st.code(result["sql"], language="sql")

        st.subheader("Result")
        st.dataframe(result["result"], use_container_width=True)

        # optional visualization
        df = result["result"]
        if df is not None and df.shape[1] >= 2:
            try:
                st.subheader("Visualization")
                st.bar_chart(df.set_index(df.columns[0]))
            except Exception:
                pass
