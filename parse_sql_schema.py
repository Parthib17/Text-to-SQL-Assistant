import sqlparse
import re

def parse_sql_schema(sql_file="schema.sql"):
    with open(sql_file, "r") as f:
        raw = f.read()

    statements = sqlparse.split(raw)
    tables = []

    for stmt in statements:
        if "CREATE TABLE" not in stmt.upper():
            continue

        match = re.search(r"CREATE TABLE\s+(\w+)", stmt, re.IGNORECASE)
        if not match:
            continue

        table_name = match.group(1)

        col_block = stmt[stmt.index("(")+1 : stmt.rindex(")")]
        col_lines = col_block.split(",")

        columns = []
        for col in col_lines:
            col = col.strip()
            if col.upper().startswith(("PRIMARY KEY", "FOREIGN KEY")):
                continue
            col_name = col.split()[0]
            columns.append(col_name)

        tables.append({
            "name": table_name,
            "columns": columns,
            "description": f"This table stores {table_name} related information."
        })

    return tables


if __name__ == "__main__":
    print(parse_sql_schema())
