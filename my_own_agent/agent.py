import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model


def _extract_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


def build_agent():
    model = init_chat_model("openai:gpt-4.1", temperature=0)
    return create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "You are a reliable local AI assistant. "
            "If information is uncertain, say so clearly and ask follow-up questions."
        ),
    )


def run_once(query: str) -> str:
    agent = build_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return _extract_text(response["messages"][-1].content)


def main() -> None:
    load_dotenv(override=True)

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Fill .env first.")

    print("My Own Agent is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You> ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        answer = run_once(user_input)
        print(f"Agent> {answer}")
