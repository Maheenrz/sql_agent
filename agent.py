import json
import os
from openai import OpenAI
from tools import tools, tool_functions
from dotenv import load_dotenv
# get OPENAI_KEY from .env

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

MODEL = "gpt-4o-mini"


# tried all of these following ,none worked as required 
# MODEL = "openrouter/auto"
# MODEL = "mistralai/mistral-7b-instruct:free"
# MODEL = "meta-llama/llama-3.1-8b-instruct:free"
# MODEL = "nex-agi/nex-n2-pro"

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
    print(f"\nQuestion: {user_question}")
    print("-" * 50)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

    max_iterations = 10

    for i in range(max_iterations):
        print(f"\n[Iteration {i+1}]")

        response = client.chat.completions.create(
            model=MODEL,
            tools=tools,
            messages=messages,
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        print(f"Stop reason: {stop_reason}")

        # agent is done — return final answer
        if stop_reason == "stop" or not message.tool_calls:
            print("\n✅ Final Answer:")
            return message.content

        # agent wants tools — process all tool calls
        # append assistant's response to history
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

        # run each tool and collect results
        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f"  → Calling: {fn_name}({fn_args})")

            fn = tool_functions[fn_name]
            result = fn(**fn_args)

            print(f"  ← Result preview: {result[:100]}...")

            # send result back
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
        answer = run_agent(question)
        print(answer)
        print("\n" + "="*60 + "\n")