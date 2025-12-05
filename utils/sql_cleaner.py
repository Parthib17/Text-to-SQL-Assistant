def clean_sql(sql):
    # If the response contains markdown code blocks, extract the content inside them
    if "```" in sql:
        parts = sql.split("```")
        if len(parts) >= 3:
            sql = parts[1]
            if sql.strip().lower().startswith("sql"):
                sql = sql.strip()[3:]
    
    return sql.strip()
