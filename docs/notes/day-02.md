# Day 02

The abstract class defines a contract.
It should not contain provider-specific implementation details.

## GroqProvider

`GroqProvider` is a concrete implementation of `LLMProvider`.

Conceptually:

```text
GroqProvider
    │
    ├── creates Groq client
    │
    ├── sends requests
    │
    └── receives Groq responses
```

The provider-specific logic should remain inside `GroqProvider`.

## Why LLMResponse Is Needed

A provider API returns a provider-specific response object.

For example, the OpenAI-compatible SDK may return data using:

```text
response.choices[0].message.content
```

Other providers may use completely different structures.

The Agent Runtime should not depend on these external response formats.
Therefore, MyOS defines its own internal response model.

## LLMResponse

Current model:

```python
@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
```

The purpose is to convert:

```text
Provider Response
        ↓
Provider-specific format
        ↓
LLMResponse
        ↓
MyOS Runtime
```

Instead of returning only:

```text
str
```

the provider should eventually return:

```text
LLMResponse
```

This allows the runtime to access:

- generated content
- model information
- input token usage
- output token usage

## Important Architectural Boundary

The desired boundary is:

```text
            MyOS Runtime
                  │
                  ▼
             LLMResponse
                  ▲
                  │
             LLMProvider
                  ▲
                  │
          Concrete Provider
                  │
                  ▼
             External API
```

The Agent should depend on MyOS contracts rather than external SDK objects.

## Why Token Usage Matters

Token usage is useful for future features such as:

- cost tracking
- latency analysis
- trajectory analysis
- adaptive reasoning
- observability

Conceptually:

```text
LLM Call
    ↓
LLMResponse
    ↓
Token Usage
    ↓
Cost / Efficiency Analysis
```

## Current Status

Implemented or designed:

- LLMProvider abstraction
- GroqProvider implementation
- LLMResponse internal model

Next step:

Convert the actual Groq API response into `LLMResponse`.

After that:

Explore tool calling.

## Key Learning

An abstraction is not useful merely because it creates more files.
Each abstraction should define a boundary.

In this case:

- `LLMProvider`: Defines how MyOS communicates with an LLM.
- `LLMResponse`: Defines how MyOS represents the result of an LLM call.
- `GroqProvider`: Handles the provider-specific implementation.
