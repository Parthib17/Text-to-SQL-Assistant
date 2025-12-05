def validate_sql(sql):
    bad = ["DROP", "DELETE", "UPDATE", "ALTER"]
    upper = sql.upper()

    for word in bad:
        if word in upper:
            return False, f"❌ Dangerous SQL blocked: {word}"

    return True, "SQL is safe."
