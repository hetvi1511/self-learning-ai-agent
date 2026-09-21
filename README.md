# Self-Learning AI Agent with Long-Term Memory

A self-learning AI agent built with **OpenAI**, **Mem0**, and **Qdrant**.

The agent can:

- remember information about the user across sessions
- retrieve relevant memories before answering
- store long-term memories locally in Qdrant
- forget specific memories
- delete all stored memories
- inspect what it currently remembers

This project is based on the architecture shown in the YouTube tutorial:

**"How to Build Self-Learning AI Agents (Python Tutorial)" by Dave Ebbelaar**

The project uses the same core idea: an AI agent becomes more personalized over time by storing and retrieving useful information from previous conversations.

## How It Works

This project does not retrain the AI model.

Instead, the agent "learns" by building a persistent memory system.

The general flow is:

```text
User sends a message
        ↓
Mem0 searches long-term memory
        ↓
Relevant memories are retrieved
        ↓
Memories + user message are sent to OpenAI
        ↓
OpenAI generates a response
        ↓
User message is analyzed by Mem0
        ↓
Useful information is extracted
        ↓
Memory is stored in Qdrant
```

When the program is restarted, the stored memories remain available.

## Architecture

```text
                    ┌───────────────────┐
                    │       User        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   AI Agent        │
                    └─────────┬─────────┘
                              │
                    Search relevant memories
                              │
                              ▼
                    ┌───────────────────┐
                    │       Mem0        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      Qdrant       │
                    │   Vector Store    │
                    └─────────┬─────────┘
                              │
                       Relevant memories
                              │
                              ▼
                    ┌───────────────────┐
                    │      OpenAI       │
                    │        LLM        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Response      │
                    └─────────┬─────────┘
                              │
                     Save useful user facts
                              │
                              ▼
                          Mem0 + Qdrant
```

## Technologies Used

### Python

Python is used to build the AI agent and connect all components together.

### OpenAI

OpenAI is used for:

- generating AI responses
- extracting useful information
- creating embeddings

### Mem0

Mem0 handles the agent's long-term memory.

It is responsible for:

- deciding what information should be remembered
- extracting useful facts from user messages
- searching stored memories
- deleting memories

### Qdrant

Qdrant is used as the local vector database.

It stores the vector representations of memories and allows semantic search.

### Docker

Docker is used to run Qdrant locally.

## Project Structure

```text
self-learning-ai-agent/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── agent.py
├── test_memory.py
├── test_local_memory.py
│
└── qdrant_storage/
```

The following files and folders are excluded from Git using `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
.DS_Store
qdrant_storage/
```

## Features

### Persistent Memory

The agent remembers useful information about the user across different sessions.

Example:

```text
You: I want to become an AI engineer.

You: My strongest programming language is Python.

You: I prefer learning by building projects.
```

After restarting the program:

```text
You: What do you remember about me?

AI:
- You want to become an AI engineer.
- Python is your strongest programming language.
- You prefer learning by building projects.
```

### Semantic Memory Search

The agent can retrieve memories even when the wording of the question is different from the wording of the saved memory.

For example, if the saved memory is:

```text
User prefers learning through projects.
```

and the user asks:

```text
What learning style works best for me?
```

the agent can still retrieve that memory because Qdrant performs vector-based semantic search.

### Memory Management

The agent includes commands for viewing and deleting stored memories.

Available commands:

```text
show memories
forget <topic>
forget everything
exit
```

## Memory Management Commands

### Show All Memories

To display everything the agent currently remembers about the user, type:

```text
show memories
```

Example output:

```text
Saved memories:

- User wants to become an AI engineer
- User prefers learning by building projects
- User's strongest programming language is Python
```

### Forget a Specific Memory

To delete a memory related to a specific topic, type:

```text
forget <topic>
```

Example:

```text
forget Python
```

The agent searches for the most relevant memory and deletes it.

Example output:

```text
Deleted memory:
User's strongest programming language is Python
```

### Forget Everything

To delete all stored memories for the current user, type:

```text
forget everything
```

Example output:

```text
All memories deleted.
```

### Exit the Agent

To stop the program, type:

```text
exit
```

## Setup Instructions

### 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/YOUR_USERNAME/self-learning-ai-agent.git
```

Then move into the project folder:

```bash
cd self-learning-ai-agent
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Create the Environment File

Create a `.env` file in the root of the project:

```bash
touch .env
```

Add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
MEM0_API_KEY=your_mem0_api_key
```

Do not upload your real `.env` file to GitHub.

The repository includes `.env.example` as a safe template.

## Running Qdrant

This project uses Qdrant as a local vector database.

Make sure Docker Desktop is installed and running before starting Qdrant.

### 1. Pull the Qdrant Docker Image

```bash
docker pull qdrant/qdrant
```

### 2. Create a Docker Volume

```bash
docker volume create qdrant_storage
```

### 3. Start Qdrant

```bash
docker run --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Leave this terminal running while using the AI agent.

### 4. Open the Qdrant Dashboard

The Qdrant dashboard is available at:

```text
http://localhost:6333/dashboard
```

The API is available at:

```text
http://localhost:6333
```

## Running the Agent

Open a new terminal while Qdrant is still running.

### 1. Activate the Virtual Environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 2. Start the Agent

Run:

```bash
python agent.py
```

You should see:

```text
Self-Learning AI Agent
----------------------

Commands:
  show memories
  forget <topic>
  forget everything
  exit
```

You can now start chatting with the agent.

### 3. Example Conversation

```text
You: I want to become an AI engineer.

AI: That's a great goal.

You: I prefer learning by building projects.

AI: Project-based learning is a good approach for AI.

You: My strongest programming language is Python.

AI: Python is especially useful for AI and machine learning.
```

To stop the agent:

```text
exit
```

### 4. Test Persistent Memory

Restart the agent:

```bash
python agent.py
```

Then ask:

```text
What do you remember about me?
```

The agent should retrieve the memories saved from the previous session.

## Testing Memory

The project includes two test files for checking memory behavior.

### 1. Test Mem0 Cloud Memory

Run:

```bash
python test_memory.py
```

This test checks whether the hosted Mem0 API can:

- save a memory
- retrieve a memory
- return the saved information correctly

### 2. Test Local Qdrant Memory

Make sure Qdrant is running first.

Then run:

```bash
python test_local_memory.py
```

This test checks whether the local memory system can:

- extract useful information with Mem0
- create embeddings with OpenAI
- store memories in Qdrant
- retrieve relevant memories from Qdrant

The local memory flow is:

```text
User message
    ↓
Mem0
    ↓
OpenAI
    ↓
Embedding
    ↓
Qdrant
    ↓
Retrieved memory
```

## Memory Design

The agent stores only the user's messages as memory candidates.

This is intentional.

For example:

```python
messages = [
    {
        "role": "user",
        "content": user_message
    }
]
```

Earlier versions of the project stored both the user's message and the assistant's response.

That can create incorrect memories because the assistant's own suggestions may later be treated as facts about the user.

For example, if the assistant says:

```text
You should build a customer support classifier.
```

Mem0 could later extract something like:

```text
User wants to build a customer support classifier.
```

even though the user never actually said that.

To reduce this problem, only user-provided information is sent to Mem0 for long-term memory extraction.

### Specific vs Broad Memory Retrieval

For specific questions, the agent uses semantic search:

```python
memory.search(
    user_message,
    filters={"user_id": USER_ID}
)
```

This retrieves memories that are semantically related to the current question.

For broad questions such as:

```text
What do you remember about me?
```

the agent uses:

```python
memory.get_all(
    filters={"user_id": USER_ID}
)
```

This allows the agent to retrieve all stored memories for the user instead of only the memories that are semantically similar to the question.

## Self-Learning vs Model Training

The term "self-learning" in this project refers to memory-based adaptation.

The underlying AI model is not retrained after every conversation.

Instead, the agent improves its responses by storing useful information and retrieving it later.

The process is:

```text
Conversation
    ↓
Useful information is extracted
    ↓
Memory is stored in Qdrant
    ↓
A future question is asked
    ↓
Relevant memories are retrieved
    ↓
The memories are added to the prompt
    ↓
The AI generates a more personalized response
```

This allows the agent to become more personalized over time without changing the model's underlying weights.

## Limitations

This project is designed as a learning and demonstration implementation.

Current limitations include:

- the agent currently uses a single user ID
- the interface is terminal-based
- Qdrant runs locally and must be started before the agent
- there is no user authentication
- memory deletion is basic
- there is no automatic memory expiration
- the agent does not score memories by importance
- the system depends on OpenAI API access and credits
- the agent does not retrain the underlying model

## Future Improvements

Possible future improvements include:

- support for multiple users
- a browser-based interface
- user authentication
- automatic memory expiration
- memory importance scoring
- memory editing
- conversation history
- cloud-hosted Qdrant
- Docker Compose setup
- deployment to a cloud platform
- agent tools and function calling

These are optional extensions and are not required for the core tutorial implementation.

## What I Learned

This project helped me understand several important AI engineering concepts, including:

- how to work with large language model APIs
- how long-term memory can be added to AI agents
- how embeddings represent semantic meaning
- how vector databases store and retrieve memories
- how semantic search differs from keyword search
- how Mem0 extracts useful information from conversations
- how Qdrant stores persistent vector memory
- how retrieved memories can be added to prompts
- how Docker can be used to run local infrastructure
- how to manage API keys securely with environment variables
- how to structure and version a project using Git and GitHub

## Security

API keys and local environment files should never be committed to GitHub.

The `.gitignore` file excludes:

```text
.env
.venv/
__pycache__/
*.pyc
.DS_Store
qdrant_storage/
```

Keep your real API keys only inside the local `.env` file.

The `.env.example` file should contain only placeholder values, for example:

```env
OPENAI_API_KEY=your_openai_key_here
MEM0_API_KEY=your_mem0_key_here
```

Never paste real API keys into source files, the README, or public GitHub commits.

## Credits

This project was inspired by:

**Dave Ebbelaar — "How to Build Self-Learning AI Agents (Python Tutorial)"**

The implementation was adapted to work with current versions of OpenAI, Mem0, and Qdrant.

## License

This project is intended for educational and portfolio use.