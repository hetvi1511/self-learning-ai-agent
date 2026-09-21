import os

from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()

memory = MemoryClient(
    api_key=os.getenv("MEM0_API_KEY")
)

USER_ID = "test_user"

results = memory.search(
    "What is my favorite programming language?",
    filters={"user_id": USER_ID}
)

for item in results["results"]:
    print(item["memory"])

#print(results)