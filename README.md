# MCP Server — AI-Powered Markdown Note Manager

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes **CRUD operations for Markdown notes** as AI tools, designed for seamless integration with **Obsidian** and other Markdown editors.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![MCP](https://img.shields.io/badge/MCP-1.27.0-green)
![License](https://img.shields.io/badge/License-MIT-orange)

</div>

---

## ✨ Features

- **📝 Full CRUD Operations** — Create, Read, Update, and Delete Markdown notes via AI tools
- **📧 Email Integration** — Send notes directly to email addresses
- **📋 Note Listing** — List all notes with metadata (filenames, modified dates)
- **🔌 Obsidian Ready** — Designed for seamless use with Obsidian and other Markdown editors
- **🤖 Local LLM Support** — Works with Ollama, LM Studio, and any OpenAI-compatible API
- **💬 AI Chat Interface** — Natural language interaction with tool-assisted responses
- **🔌 MCP Protocol** — Standardized, extensible tool protocol for AI agents

---

## 📁 Project Structure

```
MCP server/
├── Server.py          # MCP server with CRUD note tools
├── Client.py          # AI client that connects to the server
├── config.py          # Configuration (model settings)
├── requirements.txt   # Python dependencies
├── static/            # Static assets (if any)
├── Test_Files/        # Markdown notes storage directory
└── venv/              # Virtual environment (gitignored)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai) (for local LLM)
- [Obsidian](https://obsidian.md) (optional — for Markdown editing)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd "MCP server"
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   
   # macOS / Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your local LLM**

   Ensure Ollama or LM Studio is running with a model loaded. The default configuration uses:

   ```python
   # config.py
   MODEL = "qwen/qwen3.6-35b-a3b"
   ```

   Update `config.py` to match your preferred model.

---

## 📖 Usage

### Running the MCP Server

Start the server (it communicates via stdio):

```bash
python Server.py
```

The server exposes the following tools:

| Tool                | Description                                              |
|---------------------|----------------------------------------------------------|
| `create_note`       | Creates a new Markdown note with title and content       |
| `read_note`         | Reads and returns the full content of an existing note   |
| `update_note`       | Updates an existing note (with optional append mode)     |
| `delete_note`       | Permanently deletes an existing note                     |
| `list_notes`        | Lists all notes with filenames and last modified dates   |
| `send_note_via_email`| Sends a note's content to a specified email address     |

### Running the AI Client

Launch the chat interface that connects the MCP server to your local LLM:

```bash
python Client.py
```

You'll see an interactive prompt:

```
=== MCP Chat Interface Active ===
Type 'exit' or 'quit' to stop.

You: Create a note called 'project_plan' with a detailed outline.
  [SYSTEM] Calling tool: create_note...
  [SERVER] Result: Note 'project_plan.md' created successfully!

AI: I've created the note 'project_plan.md' with your outline.

You:
```

Type your message and the AI will use tools as needed. Type `exit` or `quit` to stop.

---

## 🔌 Obsidian Integration

This MCP server is designed to work alongside **Obsidian** and other Markdown-based note-taking apps. Here's how:

### Workflow

1. **Start the MCP server** — Run `python Server.py` in your terminal.
2. **Launch the AI client** — Run `python Client.py` to start the chat interface.
3. **Interact with your notes using natural language** — The AI will create, read, update, or delete notes as needed.
4. **View notes in Obsidian** — Notes are stored in the `Test_Files/` directory as `.md` files, which can be later on swithced to Obsidian Vault or any other Markdown editor folder.

### Example Prompts for Obsidian Users

- _"Create a note called 'meeting_notes' with today's discussion points"_
- _"Read my 'project_plan' note and summarize it"_
- _"Update 'project_plan' with the new deadline: December 15th"_
- _"List all my notes so I can see what's in my vault"_
- _"Send the 'report' note to john@example.com"_

### Future Obsidian Plugin (Roadmap)

We plan to build an **Obsidian Community Plugin** that:

- Connects directly to the MCP server from within Obsidian
- Provides a sidebar panel for AI-powered note management
- Allows seamless creation, editing, and deletion of notes from within Obsidian
- Supports real-time sync between Obsidian vault and MCP server
- Keeps you in Control of your notes and data.
Stay tuned for updates!

---

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# config.py
MODEL = "qwen/qwen3.6-35b-a3b"  # Change to your model name
```

Edit `Client.py` to connect to a different LLM endpoint:

```python
client = AsyncOpenAI(
    base_url="http://127.0.0.1:1234/v1",  # Your LLM endpoint
    api_key="sk-not-needed"                # Your API key (if required)
)
```

---

## 🛠️ Adding Custom Tools

To add a new tool to the server, edit `Server.py`:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name='my_new_tool',
            description='Description of what this tool does',
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "First parameter"},
                },
                "required": ["param1"]
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == 'my_new_tool':
        result = do_something(arguments['param1'])
        return [TextContent(type='text', text=str(result))]
    raise ValueError(f"Tool {name} not found")
```

---

## 📦 Dependencies

Key packages:

| Package | Purpose |
|---------|---------|
| `mcp` | Model Context Protocol server library |
| `openai` | OpenAI-compatible API client for LLM interaction |
| `fastapi` | Backend framework |
| `uvicorn` | ASGI server |

See `requirements.txt` for the full list.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) — Standardized AI tool protocol
- [Obsidian](https://obsidian.md) — Powerful Markdown note-taking app
- [Ollama](https://ollama.com) — Local LLM runtime
- [LM Studio](https://lmstudio.ai) — Local AI model server

---

**Built with ❤️ for the Markdown and AI communities.**
