import os

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import MemoryClient

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

memory = MemoryClient(
    api_key=os.getenv("MEM0_API_KEY")
)

USER_ID = "test_user"


def get_memories(user_message):
    results = memory.search(
        user_message,
        filters={"user_id": USER_ID}
    )

    memories = results.get("results", [])

    return "\n".join(
        item["memory"]
        for item in memories
    )


def generate_response(user_message):
    memories = get_memories(user_message)

    system_prompt = f"""
You are a helpful AI assistant.

Here are relevant memories about the user:

{memories}

Use these memories when relevant.
"""

    response = openai_client.responses.create(
        model="gpt-5.6-luna",
        instructions=system_prompt,
        input=user_message
    )

    return response.output_text


def save_conversation(user_message, assistant_message):
    memory.add(
        [
            {
                "role": "user",
                "content": user_message
            },
            {
                "role": "assistant",
                "content": assistant_message
            }
        ],
        user_id=USER_ID
    )


def chat():
    print("\nSelf-Learning AI Agent")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        response = generate_response(user_message)

        print(f"\nAI: {response}\n")

        save_conversation(
            user_message,
            response
        )


if __name__ == "__main__":
    chat()