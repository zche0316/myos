# Day 5 — Tool Execution and Failure Handling

## Goal

Make tool execution failures recoverable instead of crashing the entire agent runtime.

## Implemented

- ToolResult abstraction
- Tool existence checking
- Tool execution error handling
- Exception capture during tool execution
- Tool failure returned to the LLM as a ToolMessage

## Execution Flow

LLM
    ↓
ToolCall
    ↓
_execute_tool()
    ├── Tool not found
    ├── Tool success
    └── Tool exception
    ↓
ToolResult
    ↓
ToolMessage
    ↓
LLM

## Tests

### Successful Tool Execution

calculator:

123454 * 567890

Result:

70108292060

### Failed Tool Execution

failing_tool("hello")

Result:

ValueError: Intentional failure: hello

The Runtime did not crash.

The error was converted into a ToolMessage and sent back to the LLM.

## Key Understanding

Tool failure and Agent failure are different.

A tool execution error should become information available to the agent whenever possible.

The Runtime should isolate tool failures and allow the LLM to decide how to respond.
