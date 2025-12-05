from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.sql_cleaner import clean_sql

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql(question, schema_context):
    prompt = f"""
You are an expert SQL generator. Use ONLY this schema:

{schema_context}

Question: {question}

Return ONLY executable SQL. Do NOT use ```sql fences.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0
    )

    raw_sql = resp.choices[0].message.content.strip()
    return clean_sql(raw_sql)