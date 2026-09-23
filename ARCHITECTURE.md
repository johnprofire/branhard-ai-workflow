# BRANHARD AI WORKFLOW — ARCHITECTURE

## 1. System Overview

The BRANHARD AI workflow uses multiple AI agents with defined responsibilities rather than asking every model to perform the same job.

The coordinator is responsible for deciding what information is needed, which agent should handle it, and when the workflow can move to the next stage.

## 2. Agent Responsibilities

### ChatGPT
- Breaks the user's request into an actionable task.
- Creates implementation plans.
- Coordinates the other agents.
- Compares research and review results.
- Produces the workflow decision.
- Helps determine whether a task is ready for implementation or revision.

### Gemini
- Provides independent research.
- Generates alternative approaches.
- Analyzes ideas from a separate model perspective.
- Can be used to challenge assumptions before implementation.

### DeepSeek
- Provides additional analysis and research.
- Can be used for technical reasoning and alternative solutions.
- Requires active API access and available account credit.

### Claude
- Primary implementation/build agent.
- Reads the approved task and plan.
- Makes code changes.
- Runs tests.
- Fixes implementation problems.

### Grok
- Independent reviewer.
- Checks assumptions, implementation decisions, research, and potential weaknesses.
- Provides a separate review before the final decision.

### Test System
- Verifies that implementation matches the requirements.
- Runs automated and targeted tests.
- Reports failures before a task is considered complete.

### GitHub
- Stores the version-controlled project.
- Provides change history.
- Acts as the source of truth for project files.

### Journal
- Records workflow events.
- Records important decisions and errors.
- Helps reconstruct what happened during a task.

## 3. Workflow Stages

```text
TASK_CREATED
      ↓
CHATGPT_PLAN
      ↓
CLAUDE_BUILD
      ↓
GROK_REVIEW
      ↓
CHATGPT_DECIDE
      ↓
CLAUDE_FIX
      ↓
TEST_VERIFY
      ↓
GITHUB_SAVE
      ↓
COMPLETE
```

Research agents such as Gemini and DeepSeek can provide input before the decision stage.

## 4. State Management

The stage controller prevents invalid stage transitions.

Each stage records:
- sequence number
- stage
- owner
- status
- timestamp
- completion time

The workflow should not silently skip required stages.

## 5. Error Handling

An API failure should not destroy the entire workflow.

The intended system should:
1. Detect the failing agent.
2. Record the error.
3. Retry where appropriate.
4. Preserve the task and previous results.
5. Continue only when the required information is available.
6. Allow a human to intervene when necessary.

## 6. Security

Secrets must remain outside version control.

Required principle:

```text
.env → LOCAL ONLY
GitHub → NO API KEYS
```

Agents should never print or write secret values into logs, journals, reports, or generated source files.

## 7. Design Principle

No individual AI agent should silently become the sole decision-maker for major project changes.

The workflow is designed around:
- specialization
- independent review
- explicit decisions
- testing
- version control
- human oversight
