import json
import os
from openai import OpenAI
from tools import tools, tool_functions
from dotenv import load_dotenv

load_dotenv()

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    DIM     = "\033[2m"
    RED     = "\033[91m"

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are an expert data analyst for an e-commerce company.
You have access to a SQLite database with customers, products, and orders.

Your job:
1. ALWAYS call get_schema first to understand the database structure
2. Write a precise SQL query based on the schema
3. Run it with run_sql
4. Answer the user's question clearly in plain English using the results

Never guess column names. Always check the schema first.
After getting query results, answer directly — do not call any more tools."""


def run_agent(user_question: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

    max_iterations = 10

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            tools=tools,
            messages=messages,
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        if stop_reason == "stop" or not message.tool_calls:
            return message.content

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })

        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            # Show tool calls with color
            if fn_name == "get_schema":
                print(f"  {C.MAGENTA}→ Reading database schema...{C.RESET}")
            elif fn_name == "run_sql":
                query = fn_args.get("query", "")
                print(f"  {C.BLUE}→ Running SQL:{C.RESET} {C.DIM}{query}{C.RESET}")

            fn = tool_functions[fn_name]
            result = fn(**fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "Max iterations reached without a final answer."


if __name__ == "__main__":
    questions = [
        "Which customers have placed the most orders?",
        "What is the total revenue from completed orders?",
        "Which product category generates the most sales?"
    ]

    for question in questions:
        print(f"\n{C.CYAN}{C.BOLD}Q: {question}{C.RESET}")
        answer = run_agent(question)
        print(f"{C.GREEN}A: {answer}{C.RESET}")
        print("=" * 60)