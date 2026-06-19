from agent import run_agent

def main():
    print("🛒 E-Commerce SQL Agent")
    print("Ask anything about customers, orders, and products.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Goodbye.")
            break

        answer = run_agent(question)
        print(f"\nAgent: {answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()