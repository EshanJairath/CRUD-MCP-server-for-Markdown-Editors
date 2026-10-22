# Learning LangGraph

## Introduction
LangGraph is a library for building stateful, multi-actor applications with LLMs. It allows you to create complex agent workflows using a graph-based approach, where nodes represent actions (like LLM calls or tool usage) and edges define the flow of control.

## Key Concepts
- **State**: The current state of the graph (variables, data, context).
- **Nodes**: The building blocks of your graph (LLM calls, tools, logic).
- **Edges**: The connections between nodes that determine the flow.
- **Cycles**: LangGraph supports loops, making it ideal for agents that need to iterate (e.g., search -> check -> refine).

## Installation
```bash
pip install langgraph langchain-openai
```

## Basic Example
A simple agent graph might look like this:
1. Start Node: Receive user query.
2. Agent Node: Call LLM with tools.
3. Conditional Edge: If tool result is needed, go back to Agent; otherwise, go to End Node.

## Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain AI GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Tutorials](https://python.langchain.com/docs/langgraph)

## Next Steps
- [ ] Install dependencies
- [ ] Build a simple ReAct agent
- [ ] Explore state management
- [ ] Add conditional routing