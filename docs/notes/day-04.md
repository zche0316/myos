# Day 4 — Message Abstraction

## Goal

Replace raw message dictionaries with typed message objects.

## Implemented

- UserMessage
- SystemMessage
- AssistantMessage
- ToolMessage
- ToolCall
- LLMResponse
- Provider message conversion
- Proper tool-call message loop

## Message Flow

UserMessage
    ↓
LLM
    ↓
AssistantMessage + ToolCall
    ↓
Tool execution
    ↓
ToolMessage
    ↓
LLM
    ↓
AssistantMessage

## Key Understanding

The Runtime operates on MyOS-level Message objects.

The Provider is responsible for converting:

MyOS Message → Provider/API format
Provider/API response → MyOS Message

The Runtime should not depend on Groq/OpenAI-specific message formats.
