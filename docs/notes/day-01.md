# Day 01 — First LLM Call

## Goal

Run the first LLM request through Groq.

---

## What I Did

- Created the initial Python environment.
- Configured the Groq API key.
- Used the OpenAI-compatible SDK.
- Sent a basic prompt to an LLM.
- Observed the returned response.

---

## Basic Flow

Python Program
    ↓
OpenAI-compatible SDK
    ↓
Groq API
    ↓
LLM
    ↓
Response

---

## Important Observation

The LLM API response contains more information than the generated text.

The response may include:

- message content
- model information
- token usage
- completion metadata

Example conceptual structure:

Response
├── choices
│   └── message
│       └── content
│
├── model
│
└── usage
    ├── prompt_tokens
    └── completion_tokens

---

## Key Learning

Calling an LLM API is only one part of building an agent.

A simple LLM application is:

Input
    ↓
LLM
    ↓
Text

An agent requires a decision and execution loop.

Eventually:

Input
    ↓
LLM
    ↓
Decision
    ↓
Tool
    ↓
Observation
    ↓
LLM

---

## Questions for Future Development

- How should different LLM providers be abstracted?
- How should LLM responses be represented internally?
- How can the agent call tools?
- How should tool results return to the LLM?
- How should token usage and cost be tracked?

---

## Outcome

Successfully completed the first direct LLM call.