import os

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

load_dotenv()

# OpenAI client used to generate chatbot responses
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Mem0 configuration using local Qdrant
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "self_learning_agent",
            "host": "localhost",
            "port": 6333
        }
    },

    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-mini"
        }
    },

    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }
}

memory = Memory.from_config(config)

USER_ID = "test_user"


def get_memories(user_message):
    """
    Retrieve memories relevant to the current user message.

    If the user asks broadly what the agent remembers,
    return all memories instead of doing semantic search.
    """

    if "what do you remember about me" in user_message.lower():
        results = memory.get_all(
            filters={"user_id": USER_ID}
        )
    else:
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
    """
    Generate an AI response using relevant long-term memories.
    """

    memories = get_memories(user_message)

    system_prompt = f"""
You are a helpful AI assistant.

Here are relevant memories about the user:

{memories}

Use these memories when they are relevant to the user's question.

Do not mention the memory system unless the user specifically asks
how memory works.
"""

    response = openai_client.responses.create(
        model="gpt-5.6-luna",
        instructions=system_prompt,
        input=user_message
    )

    return response.output_text


def save_conversation(user_message, assistant_message):
    """
    Save useful information from the user's message.

    We only send the user's message to Mem0 so that the
    assistant's own suggestions are not accidentally stored
    as facts about the user.
    """

    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    memory.add(
        messages,
        user_id=USER_ID
    )


def show_memories():
    """
    Display all memories currently stored for this user.
    """

    results = memory.get_all(
        filters={"user_id": USER_ID}
    )

    memories = results.get("results", [])

    if not memories:
        print("\nNo memories saved.\n")
        return

    print("\nSaved memories:")

    for item in memories:
        print(f"- {item['memory']}")

    print()


def forget_memory(query):
    """
    Find a memory related to the query and delete it.
    """

    results = memory.search(
        query,
        filters={"user_id": USER_ID}
    )

    memories = results.get("results", [])

    if not memories:
        print("\nNo matching memory found.\n")
        return

    memory_to_delete = memories[0]

    memory.delete(
        memory_to_delete["id"]
    )

    print(
        f"\nDeleted memory: {memory_to_delete['memory']}\n"
    )


def forget_all_memories():
    """
    Delete all memories associated with this user.
    """

    results = memory.get_all(
        filters={"user_id": USER_ID}
    )

    memories = results.get("results", [])

    if not memories:
        print("\nNo memories to delete.\n")
        return

    for item in memories:
        memory.delete(
            item["id"]
        )

    print("\nAll memories deleted.\n")


def chat():
    """
    Main chatbot loop.
    """

    print("\nSelf-Learning AI Agent")
    print("----------------------")
    print("Commands:")
    print("  show memories")
    print("  forget <topic>")
    print("  forget everything")
    print("  exit")
    print()

    while True:
        user_message = input("You: ").strip()

        if not user_message:
            continue

        # Exit
        if user_message.lower() == "exit":
            print("\nGoodbye!")
            break

        # Show all memories
        if user_message.lower() == "show memories":
            show_memories()
            continue

        # Delete all memories
        if user_message.lower() == "forget everything":
            forget_all_memories()
            continue

        # Delete a specific memory
        if user_message.lower().startswith("forget "):
            query = user_message[7:].strip()

            if not query:
                print(
                    "\nTell me what you want me to forget.\n"
                )
                continue

            forget_memory(query)
            continue

        # Normal conversation
        response = generate_response(
            user_message
        )

        print(f"\nAI: {response}\n")

        # Save user information after responding
        save_conversation(
            user_message,
            response
        )


if __name__ == "__main__":
    chat()