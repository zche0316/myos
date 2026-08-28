# MyOS Roadmap

## Stage 1 — Minimal Agent Core

### Goal

Build a minimal but complete agent loop.

### Milestones

#### M1 — LLM Foundation

- [x] Call Groq API
- [x] Observe raw LLM response
- [x] Create LLMProvider interface
- [x] Create GroqProvider
- [x] Define LLMResponse
- [ ] Convert Groq responses into LLMResponse
- [ ] Add basic Message abstraction

#### M2 — Tool System

- [ ] Define Tool abstraction
- [ ] Define ToolCall model
- [ ] Define ToolResult model
- [ ] Implement ToolRegistry
- [ ] Implement ToolExecutor
- [ ] Implement calculator tool
- [ ] Test LLM tool calling

#### M3 — Agent Loop

- [ ] Implement Agent
- [ ] Implement message history
- [ ] Implement tool-call loop
- [ ] Add stop conditions
- [ ] Add maximum iteration limit
- [ ] Handle basic errors

### Expected Result

A user can run:

myos

Then:

User
 ↓
LLM
 ↓
Tool decision
 ↓
Tool execution
 ↓
LLM
 ↓
Final answer

---

# Stage 2 — Engineering the Runtime

## Context

- [ ] Message model
- [ ] Session model
- [ ] Context window management
- [ ] Conversation summarisation
- [ ] Token estimation

## Observability

- [ ] LLM call logging
- [ ] token tracking
- [ ] latency tracking
- [ ] tool execution logging
- [ ] execution trace

## Evaluation

- [ ] Basic agent test tasks
- [ ] Tool-use benchmark
- [ ] Failure logging

### Expected Result

MyOS becomes debuggable and measurable.

---

# Stage 3 — Productive Agent Capabilities

## MCP

- [ ] MCP client
- [ ] MCP server discovery
- [ ] MCP tool integration

## Skills

- [ ] Skill definition
- [ ] Skill loader
- [ ] Skill metadata
- [ ] Skill selection

## Workflow

- [ ] Multi-step workflows
- [ ] Task planning
- [ ] Workflow execution

### Expected Result

MyOS can connect to useful external systems.

---

# Stage 4 — Memory and Personalisation

## Lightweight Memory

- [ ] Memory candidate extraction
- [ ] Importance scoring
- [ ] Persistent storage
- [ ] Memory retrieval
- [ ] Context injection

## User Profile

- [ ] Preference extraction
- [ ] Structured user profile
- [ ] Profile update policy

Important:

Memory should be evaluated experimentally.

Avoid storing everything.

---

# Stage 5 — Subagents

- [ ] Agent delegation interface
- [ ] Specialist agent roles
- [ ] Result aggregation
- [ ] Cost tracking

Experiments:

- Single agent vs subagent
- When delegation helps
- When delegation hurts

---

# Stage 6 — Adaptive Agent Execution

Research-oriented stage.

- [ ] Reasoning cost tracking
- [ ] Confidence estimation
- [ ] Verification action
- [ ] Retrieval action
- [ ] Early stopping
- [ ] Adaptive action selection

Potential controller:

AgentState
    ↓
Controller
    ↓
Choose:
    Think
    Verify
    Retrieve
    Delegate
    Stop

---

# Stage 7 — Harness Improvement

Long-term.

- [ ] Trajectory dataset
- [ ] Failure classification
- [ ] Prompt optimisation experiments
- [ ] Skill improvement
- [ ] Strategy comparison
- [ ] Automated evaluation

---

# Suggested Timeline

The timeline is flexible.

## Month 1

Focus:

Minimal Agent Core

Target:

A working tool-calling agent.

---

## Month 2

Focus:

Runtime Engineering

Target:

Context, sessions and observability.

---

## Month 3

Focus:

MCP and Skills

Target:

Connect MyOS to useful external workflows.

---

## Month 4

Focus:

Memory and Personalisation

Target:

Lightweight persistent memory.

---

## Month 5

Focus:

Subagents

Target:

Task delegation experiments.

---

## Month 6+

Focus:

Adaptive execution and self-improving harness.

This stage should remain experimental.