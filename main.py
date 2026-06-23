from agent import run_agent

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

def print_banner():
    print(f"\n{C.CYAN}{C.BOLD}{'═' * 54}{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}   🛒  SQL Agent — E-Commerce Intelligence{C.RESET}")
    print(f"{C.DIM}   Natural language → SQL → Answer{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}{'═' * 54}{C.RESET}\n")
    print(f"{C.DIM}   Ask anything about customers, orders, products.{C.RESET}")
    print(f"{C.DIM}   Type 'exit' to quit.\n{C.RESET}")

def print_divider():
    print(f"{C.DIM}{'─' * 54}{C.RESET}")

def main():
    print_banner()

    while True:
        try:
            question = input(f"{C.BOLD}{C.CYAN}You › {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.DIM}Goodbye! 👋{C.RESET}\n")
            break

        if not question:
            continue

        if question.lower() in ["exit", "quit", "q"]:
            print(f"\n{C.DIM}Goodbye! 👋{C.RESET}\n")
            break

        print(f"\n{C.YELLOW}⚙  Running agent...{C.RESET}\n")
        answer = run_agent(question)

        print(f"\n{C.GREEN}{C.BOLD}Agent › {C.RESET}{answer}\n")
        print_divider()

if __name__ == "__main__":
    main()