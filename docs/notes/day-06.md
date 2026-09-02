# Day 6 — Session & Conversation History

## Goal

Enable the agent to remember what happened in the current conversation and keep that state separate from tool execution.

## Implemented

- Added the concept of AgentSession
- Stored message history inside the session
- Changed runtime execution from run(messages) to run(session)
- Decoupled Session from Runtime
- Preserved assistant and tool messages in the conversation history
- Verified multi-turn memory through repeated user questions

## Session Design

A session is simply a container for the current conversation state:

```python
class AgentSession:
    id: str
    messages: list[Message]
```

Example:

```text
Session
├── id
└── messages
    ├── UserMessage
    ├── AssistantMessage
    ├── UserMessage
    └── AssistantMessage
```

## Runtime Flow

```text
User
 ↓
Session.messages.append(UserMessage)
 ↓
AgentRuntime.run(session)
 ↓
LLM
 ↓
Tool Call / Final Answer
 ↓
Session.messages.append(...)
```

The runtime is responsible for execution, while the session is responsible for state.

## Why This Matters

Without a session, the app only receives a list of messages and cannot distinguish between:

- different users
- different conversations
- previous turns in the same chat
- which messages already happened in the current run

The key change is:

```python
runtime.run(session)
```

instead of:

```python
runtime.run(messages)
```

## Multi-turn Conversation

Example:

```text
User: My name is Chen.
Assistant: Nice to meet you, Chen!

User: What is my name?
Assistant: Your name is Chen.
```

This works because the LLM receives the full conversation history each time.

The model is not magically remembering previous calls by itself; the application sends:

```text
[UserMessage, AssistantMessage, UserMessage]
```

again to the LLM for the next round.

## Important Detail

When a final response is returned, it must also be appended to the session:

```python
if not response.tool_calls:
    session.messages.append(response.message)
    return response.content or ""
```

Otherwise the assistant's previous answer will not be visible in the next turn.

## Tool Messages in Session

The full execution history also belongs in the session:

```text
UserMessage
  ↓
AssistantMessage(tool_calls=[...])
  ↓
ToolMessage
  ↓
AssistantMessage(final)
```

So session history is not only a chat log; it is the full agent execution history.

## Session vs Memory vs Persistence

### Session

Current conversation state.

### Long-Term Memory

Useful facts worth keeping across sessions.

### Persistence

Saving session data to disk or a database later.

This day only covers in-memory session state, not permanent storage.

## Test Result

I tested a four-round conversation:

1. User: My name is Chen.
2. User: What is my name?
3. User: What did I tell you at the beginning?
4. User: What did you answer me in the previous round?

The assistant answered correctly each time using the previous conversation history.

## Key Understanding

Session and Runtime are different responsibilities:

```text
Session = state
Runtime = execution
```

The agent becomes a stateful system instead of a one-shot function call.

## Outcome

MyOS can now support multi-turn conversation history within a session, and the runtime can run repeatedly for different sessions without being tied to a single conversation state.

## Checklist

Day 1  LLM API                  ✓
Day 2  Provider Abstraction    ✓
Day 3  Tool Calling             ✓
Day 4  Message Abstraction      ✓
Day 5  Tool Failure Handling    ✓
Day 6  Session + Conversation   ✓
Day 7  Persistence              → Next
Day 8  Context / Token Budget
Day 9  Context Compaction
Day 10 Long-Term Memory
Day 11 Skills
Day 12 MCP
Day 13 Workflow
Day 14 Adaptive Reasoning
Day 15 Multi-Agent
Day 16 Agent Harness / Self-Evolution