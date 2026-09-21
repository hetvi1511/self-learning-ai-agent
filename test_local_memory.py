from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

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

results = memory.search(
    "How do I prefer to learn AI?",
    filters={"user_id": USER_ID}
)

print("\nRetrieved memories:")

for item in results["results"]:
    print(item["memory"])