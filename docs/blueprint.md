# MyOS Blueprint

## 1. Project Vision

MyOS is a personal AI agent runtime and harness designed to explore how modern AI agents can be built from first principles.

The project is not intended to be a general-purpose operating system.

Instead, MyOS aims to become a modular personal agent environment that can:

- communicate with LLMs through interchangeable providers
- execute tools and external actions
- connect to MCP servers
- manage short-term and long-term context
- maintain user and task-related memory
- load reusable skills
- coordinate subagents
- make adaptive decisions about reasoning and execution
- record and analyse agent trajectories
- gradually support workflow automation and personal productivity

The project will be developed incrementally.

The first objective is not to build a complex autonomous agent.

The first objective is to understand and implement the minimal execution loop:

User Input
    ↓
LLM
    ↓
Decision
    ↓
Tool Call
    ↓
Tool Execution
    ↓
Observation
    ↓
LLM
    ↓
Final Answer

From this minimal loop, more advanced capabilities will be added progressively.

---

# 2. Core Design Principles

## 2.1 Learn by Building

MyOS is primarily a learning-oriented engineering project.

Major abstractions should not be copied blindly from existing projects.

Instead, each abstraction should first be implemented in a minimal form and then compared with mature systems such as:

- pi
- Claude Code
- OpenAI Codex
- LangGraph
- OpenHands

The purpose is to understand why production agent systems are structured the way they are.

---

## 2.2 Start Minimal

Do not implement future features before they are required.

For example:

Do not create:

- multi-agent systems
- vector databases
- complex memory systems
- distributed execution
- workflow orchestration

before the basic agent loop works.

The project should evolve in layers.

---

## 2.3 Provider Independence

The Agent Runtime should not depend directly on:

- Groq
- OpenAI
- Anthropic
- a specific SDK

Instead:

Agent
    ↓
LLMProvider Interface
    ↓
Concrete Provider
    ↓
External LLM API

All provider-specific response formats should be converted into MyOS internal models.

---

## 2.4 Internal Data Contracts

MyOS should define its own internal representations.

For example:

LLMResponse

ToolCall

ToolResult

Message

AgentState

Trajectory

The Agent Runtime should depend on these internal contracts rather than external SDK objects.

---

## 2.5 Observability First

Agent systems are difficult to debug.

Important events should eventually be observable.

For each LLM call, MyOS should aim to record:

- model
- input tokens
- output tokens
- latency
- tool calls
- tool results
- errors
- retries

This data will later support:

- debugging
- evaluation
- cost analysis
- trajectory analysis
- adaptive reasoning

---

# 3. Long-Term Architecture

The intended architecture is:

                    ┌───────────────┐
                    │      CLI      │
                    │   / Interface │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Agent     │
                    │    Runtime    │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      LLM Layer         Tool Layer        Context Layer
          │                 │                 │
          ▼                 ▼                 ▼
      Providers         Tool Registry     Context Manager
          │                 │                 │
          ▼                 ▼                 ▼
    Groq/OpenAI       Tool Executor       Compression
    Anthropic/Local                         Summaries
                                              │
                                              ▼
                                          Memory Layer
                                              │
                                  ┌───────────┴───────────┐
                                  │                       │
                                  ▼                       ▼
                            Short-Term               Long-Term
                             Memory                    Memory
                                                        │
                                                        ▼
                                                 User Profile

Additional layers may include:

- MCP
- Skills
- Subagents
- Workflow Engine
- Evaluation
- Observability
- Adaptive Controller

---

# 4. Development Layers

MyOS will be developed in progressive layers.

## Layer 1 — LLM Runtime

Goal:

Build a clean abstraction for interacting with LLM providers.

Core components:

- LLMProvider
- GroqProvider
- LLMResponse
- Message model
- token usage tracking

Current status:

In progress.

---

## Layer 2 — Tool System

Goal:

Allow the LLM to request actions.

Core components:

- Tool abstraction
- Tool definition
- Tool registry
- Tool executor
- Tool result

Target execution flow:

User
 ↓
LLM
 ↓
ToolCall
 ↓
Tool Validation
 ↓
Tool Execution
 ↓
ToolResult
 ↓
LLM

Example tools:

- calculator
- file read
- file write
- shell command
- web search

---

## Layer 3 — Agent Runtime

Goal:

Build the minimal agent execution loop.

Core components:

- Agent
- AgentState
- Message history
- execution loop
- stop conditions
- maximum iteration limits

Basic loop:

while not finished:

    response = llm.generate(messages)

    if response contains tool call:
        execute tool
        append observation
    else:
        return final answer

---

## Layer 4 — Context Management

Goal:

Prevent context from growing indefinitely.

Features:

- message window management
- token estimation
- conversation summarisation
- context compression
- selective history retrieval

Questions to explore:

- Which messages should remain in context?
- When should old messages be summarised?
- When should information be removed?
- How much context is enough?

---

## Layer 5 — Memory

Goal:

Provide persistent information beyond a single conversation.

Memory should remain a lightweight feature rather than the main focus of early development.

Potential memory categories:

### Episodic Memory

Past interactions and events.

Example:

User previously created a Python project.

### Semantic Memory

General facts derived from interactions.

Example:

User prefers a particular programming style.

### Procedural Memory

Reusable knowledge about how to perform tasks.

Example:

A previously successful workflow.

### User Profile

Structured information about the user's preferences and working patterns.

Example:

Preferred programming language.

Preferred project structure.

Memory pipeline:

Interaction
    ↓
Memory Candidate
    ↓
Importance Evaluation
    ↓
Store / Discard
    ↓
Retrieval
    ↓
Context Injection

Important principle:

Memory should improve agent performance.

It should not simply become an unlimited database of conversations.

---

## Layer 6 — MCP

Goal:

Connect MyOS with external tool ecosystems.

Potential capabilities:

MyOS
  ↓
MCP Client
  ↓
External MCP Servers
  ├── Filesystem
  ├── GitHub
  ├── Database
  └── Other Services

MCP should reuse the internal Tool abstraction where possible.

---

## Layer 7 — Skills

Goal:

Support reusable capability packages.

A Skill may contain:

- instructions
- prompts
- tools
- examples
- workflows
- metadata

Conceptually:

Skill
 ├── Instructions
 ├── Tools
 ├── Context
 └── Workflow

Example:

Code Review Skill

GitHub Issue Analysis Skill

Research Skill

---

## Layer 8 — Subagents

Goal:

Allow tasks to be delegated to specialised agents.

Possible roles:

- researcher
- coder
- reviewer
- planner

However:

Do not create multiple agents simply because multi-agent systems are fashionable.

Subagents should be introduced only when task decomposition provides a measurable benefit.

---

## Layer 9 — Adaptive Execution

Goal:

Allow MyOS to decide how much computation a task deserves.

Inspired by recent research on:

- test-time compute
- reasoning allocation
- verification
- early stopping
- value of computation

Potential decisions:

Should the agent:

- answer now?
- think longer?
- generate another candidate?
- verify the result?
- call a tool?
- retrieve information?
- delegate to a subagent?
- stop?

This layer should use information such as:

- estimated confidence
- task difficulty
- previous failures
- token cost
- latency
- verification results

Concept:

                Agent State
                     │
                     ▼
             Adaptive Controller
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Think        Verify       Retrieve
        │
        ▼
       Stop

---

## Layer 10 — Self-Improving Harness

Long-term experimental direction.

Goal:

Allow MyOS to improve its execution strategies based on past trajectories.

Possible mechanisms:

Trajectory
    ↓
Evaluation
    ↓
Failure Analysis
    ↓
Strategy Update
    ↓
Future Execution

Possible learning targets:

- better tool selection
- better prompts
- better context selection
- better skill selection
- better stopping decisions

This is a long-term research and engineering goal.

It should not be implemented prematurely.

---

# 5. Target Repository Structure

The intended repository structure is:

myos/

├── README.md
├── pyproject.toml
├── .env
├── .gitignore
│
├── src/
│   └── myos/
│       │
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── llm/
│       │   ├── provider.py
│       │   ├── groq.py
│       │   ├── models.py
│       │   └── messages.py
│       │
│       ├── agent/
│       │   ├── agent.py
│       │   ├── loop.py
│       │   └── state.py
│       │
│       ├── tools/
│       │   ├── tool.py
│       │   ├── registry.py
│       │   ├── executor.py
│       │   └── models.py
│       │
│       ├── context/
│       │
│       ├── memory/
│       │
│       ├── mcp/
│       │
│       ├── skills/
│       │
│       ├── subagents/
│       │
│       ├── evaluation/
│       │
│       ├── observability/
│       │
│       └── config/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── blueprint.md
│   ├── roadmap.md
│   ├── architecture.md
│   │
│   └── notes/
│       ├── day-01.md
│       └── day-02.md
│
├── examples/
│
└── references/

Important rule:

Do not create all directories immediately.

Create a module when the project actually begins implementing that capability.

The structure above represents the intended architecture rather than the current implementation.

---

# 6. Current Implementation Status

Current development stage:

Stage 1 — Minimal Agent Runtime

Completed:

- Python environment setup
- Groq API access
- basic LLM request
- response observation

In progress:

- LLMProvider abstraction
- GroqProvider implementation
- LLMResponse internal model

Next:

- Tool abstraction
- Tool call parsing
- Tool registry
- Tool execution
- minimal Agent Loop

---

# 7. Reference Projects

MyOS should learn from existing systems without copying their architecture blindly.

Primary references:

## pi

Study:

- minimal agent loop
- provider abstraction
- tool architecture
- context management

## Claude Code

Study:

- production agent architecture
- coding tools
- context handling
- agent execution loop

## LangGraph

Study:

- state-based agent execution
- workflow orchestration
- graph-based control flow

## OpenHands

Study:

- coding agents
- sandbox execution
- agent trajectories

The goal is to understand the architectural reasons behind their design decisions.

---

# 8. Success Criteria

The project should gradually achieve:

Level 1:

A minimal LLM wrapper.

Level 2:

An agent capable of calling local tools.

Level 3:

A reliable tool execution loop.

Level 4:

Context and session management.

Level 5:

MCP and reusable skills.

Level 6:

Subagent delegation.

Level 7:

Adaptive reasoning and execution.

Level 8:

Trajectory-based evaluation and self-improvement.

---

# 9. Non-Goals

The following should not be priorities during the early stages:

- building a complete autonomous operating system
- building a full multi-agent company
- creating a complex vector database infrastructure
- reproducing Claude Code
- reproducing OpenAI Codex
- implementing distributed agent infrastructure

The primary objective is:

Understand how modern AI agents work by implementing the critical abstractions progressively.