import sqlite3
import json

DB_PATH = "ecommerce.db"

def get_schema() -> str:
    """Returns the database schema — all tables and their columns."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # get all table names
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        # tables = [("customers",), ("products",), ("orders",)]

        schema = {}

        for (table_name,) in tables:
            # for each table, get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            # each row: (id, name, type, notnull, default, pk)

            schema[table_name] = [
                {"column": col[1], "type": col[2]}
                for col in columns
            ]

        return json.dumps(schema, indent=2)
    




def run_sql(query: str) -> str:
    """Executes a SQL SELECT query and returns the results."""

    # safety check — only allow SELECT queries
    # never let an agent DROP or DELETE your data
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(query)

            rows = cursor.fetchall()

            # get column names from cursor description
            columns = [description[0] for description in cursor.description]

            # zip columns with each row to make readable dicts
            result = [dict(zip(columns, row)) for row in rows]

            return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})    
    



def format_result(data: str) -> str:
    """Formats raw JSON query results into a clean, readable summary."""
    try:
        parsed = json.loads(data)

        if isinstance(parsed, dict) and "error" in parsed:
            return f"Error: {parsed['error']}"

        if not parsed:
            return "No results found."

        if len(parsed) == 1:
            # single row — format as key: value pairs
            row = parsed[0]
            lines = [f"{k}: {v}" for k, v in row.items()]
            return "\n".join(lines)

        # multiple rows — format as numbered list
        lines = []
        for i, row in enumerate(parsed, start=1):
            row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
            lines.append(f"{i}. {row_str}")

        return "\n".join(lines)

    except Exception as e:
        return f"Could not format result: {str(e)}"
    


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_schema",
            "description": "Get the database schema — all table names and their columns. Always call this first before writing any SQL query.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": "Execute a SQL SELECT query on the ecommerce database and return raw results as JSON.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A valid SQLite SELECT query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

tool_functions = {
    "get_schema": get_schema,
    "run_sql": run_sql,
} 



if __name__ == "__main__":
    print("=== SCHEMA ===")
    print(get_schema())

    print("\n=== SQL RESULT ===")
    result = run_sql("SELECT name, city FROM customers LIMIT 3")
    print(result)

    print("\n=== FORMATTED ===")
    print(format_result(result))