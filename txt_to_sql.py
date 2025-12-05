import os
from dotenv import load_dotenv
import openai
from database import execute_query

load_dotenv()

def clean_sql(sql):
    # If the response contains markdown code blocks, extract the content inside them
    if "```" in sql:
        parts = sql.split("```")
        if len(parts) >= 3:
            sql = parts[1]
            if sql.strip().lower().startswith("sql"):
                sql = sql.strip()[3:]
    
    return sql.strip()

def question_to_sql(question):
    
    system_prompt = "You are an expert SQL generator. Output ONLY the raw SQL query for the given question. Do not output markdown formatting (like ```sql), explanations, or any other text."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0,
        max_tokens=200
    )

    sql = response.choices[0].message.content.strip()
    return clean_sql(sql)


if __name__ == "__main__":
    question = "Which customers are located in london?"
    sql = question_to_sql(question)
    df = execute_query(sql)
    print(df)