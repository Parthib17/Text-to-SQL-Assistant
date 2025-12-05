from agents.retriever import retrieve_schema
from agents.sql_generator import generate_sql
from agents.critic import validate_sql
from agents.sql_executor import run_sql

def answer_question(question):
    # Step 1: Retrieve schema
    schema = retrieve_schema(question)

    # Step 2: Generate SQL
    sql = generate_sql(question, schema)

    # Step 3: Validate SQL
    ok, msg = validate_sql(sql)
    if not ok:
        return sql, msg, None

    # Step 4: Execute SQL
    df = run_sql(sql)

    return sql, msg, df
