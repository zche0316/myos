# MyOS Development Principles

## 1. Do Not Overengineer

Do not implement future features before they are required.

Prefer:

small working implementation

over:

large speculative architecture.

---

## 2. Understand Before Copying

Reference projects such as pi and Claude Code are used for learning.

Do not copy their architecture blindly.

First implement a minimal version.

Then compare the design with mature projects.

---

## 3. Preserve Architectural Boundaries

External SDK objects should not leak deeply into the runtime.

Examples:

Groq Response
    ↓
GroqProvider
    ↓
LLMResponse

Do not allow:

Agent
    ↓
OpenAI SDK response

directly.

---

## 4. Keep the Agent Loop Explicit

The core execution flow should remain understandable.

User
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

Avoid hiding the main execution loop behind unnecessary abstractions.

---

## 5. Add Observability Early

Important events should eventually be measurable.

Track:

- LLM calls
- token usage
- latency
- tool calls
- errors

---

## 6. Prefer Incremental Commits

Each development milestone should ideally correspond to a small Git commit.

Examples:

feat: add groq provider

feat: add llm response model

feat: add tool abstraction

feat: add tool registry

feat: implement agent loop