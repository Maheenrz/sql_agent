# SQL Agent 🛒
> Natural language → SQL → Answer. Built with raw OpenAI tool calling — no LangChain, no frameworks.

Ask this agent anything about an e-commerce database in plain English. It reasons about the schema, writes the SQL, executes it, and answers — autonomously.

---

## Why this is different from a chatbot

Most "AI + database" demos hardcode the SQL or use an ORM wrapper. This agent:
- Has **zero knowledge** of the database structure at start
- Calls `get_schema` first, every time, to understand what exists
- Writes SQL dynamically based on what it finds
- Executes it live against a real SQLite database
- Returns a plain English answer grounded in real data

No hallucination. No hardcoded queries. Pure tool-calling loop.

---

## Architecture

```
User question (natural language)
        ↓
GPT-4o-mini (via GitHub Models)
        ↓
┌─────────── Tool Loop ───────────┐
│                                  │
│  get_schema()    run_sql()       │
│  ↓ table names   ↓ SELECT query  │
│  ↓ column types  ↓ live results  │
└──────────────────────────────────┘
        ↓
Final Answer (plain English)
```

---

## Tools

| Tool | What it does |
|------|-------------|
| `get_schema` | Reads all tables and columns from SQLite via PRAGMA. Agent always calls this first. |
| `run_sql` | Executes any SELECT query. Blocks DROP/DELETE/UPDATE for safety. Returns JSON rows. |

`format_result` intentionally excluded from the tools list — leaving it in caused the agent to loop unnecessarily after getting results.

---

## Database

Seeded SQLite e-commerce database with:
- **8 customers** across Lahore, Karachi, Islamabad, Faisalabad
- **8 products** across Electronics, Footwear, Clothing, Beauty, Accessories
- **50 orders** with randomized dates, quantities, and statuses (completed / pending / cancelled)

---

## Stack

- **OpenAI SDK** — raw tool calling (function calling API)
- **GitHub Models** — free GPT-4o-mini inference endpoint
- **SQLite** — local database, zero setup
- **Python 3.11** — no frameworks

---

## Run it

```bash
git clone https://github.com/Maheenrz/sql_agent
cd sql_agent
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add GitHub token (free at github.com/settings/tokens)
echo "GITHUB_TOKEN=your_token_here" > .env

# Seed the database
python database.py

# Run the agent
python main.py
```

---

## Sample queries to try

```
Which customers have placed the most orders?
What is the total revenue from completed orders?
Which product category generates the most sales?
Which city has the highest average order value?
Show me all pending orders with customer names and product details.
```

---

## Sample output

```
You › Which product category generates the most sales?

  → Reading database schema...
  → Running SQL: SELECT p.category, SUM(o.total_price) as revenue
                 FROM orders o JOIN products p ON o.product_id = p.id
                 WHERE o.status = 'completed'
                 GROUP BY p.category ORDER BY revenue DESC

Agent › Electronics generates the most sales with a total revenue of
        Rs. 2,847,000 from completed orders, followed by Footwear
        at Rs. 312,500.
```

---

## Key concepts demonstrated

- **Raw tool calling** — OpenAI function calling API without any framework
- **Agentic loop** — agent runs until `finish_reason == stop`, not a fixed number of steps
- **Schema-first reasoning** — agent never assumes column names, always inspects first
- **Safety guardrails** — only SELECT queries allowed, enforced at the tool level
- **No framework dependency** — entire agent loop is ~60 lines of plain Python

---

## What I'd add next

- Multi-table JOIN suggestions when query is ambiguous
- Query result caching for repeated questions
- Write operations with confirmation step (INSERT/UPDATE with human-in-the-loop)
- FastAPI wrapper to serve as a REST endpoint
- Evaluation suite — test 20 questions, measure SQL accuracy