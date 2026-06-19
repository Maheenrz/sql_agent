# SQL Agent — Natural Language to SQL

An agentic AI system that answers questions about an e-commerce 
database in plain English using tool calling.

## How it works
1. User asks a question in plain English
2. Agent calls `get_schema` to understand the database structure  
3. Agent writes and runs a precise SQL query via `run_sql`
4. Agent returns a clean answer in natural language

## Tech Stack
- Python, SQLite, OpenAI SDK
- GitHub Models (GPT-4o mini) for inference
- Agentic loop with multi-step tool calling

## Run locally
pip install openai python-dotenv
cp .env.example .env  # add your GITHUB_TOKEN
python database.py    # seed the database
python main.py        # start the agent