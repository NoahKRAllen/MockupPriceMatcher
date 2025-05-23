from langchain_ollama.llms import OllamaLLM
from langgraph_router import run_router

llm = OllamaLLM(model="gemma3")

def main():
    while True:
        query = input("What can I help you with?")
        print("[DEBUG] input_dict passed to smart_router:", query)
        if query.lower() in ["exit", "quit", "close"]:
            break

        response = run_router(query)
        print(response["result"])


if __name__ == "__main__":
    main()