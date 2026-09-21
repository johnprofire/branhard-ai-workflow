# BRANHARD AI WORKFLOW — SETUP

## Prerequisites

The workflow is designed for an environment capable of running:

- Python 3
- Git
- Node/npm where required by supporting tools
- Internet access for API requests

## Environment Variables

Create a local `.env` file.

Example:

```env
OPENAI_API_KEY=YOUR_KEY
DEEPSEEK_API_KEY=YOUR_KEY
GEMINI_API_KEY=YOUR_KEY
```

Additional provider variables can be added as integrations are completed.

Never commit the `.env` file.

## Recommended .gitignore

The repository should include:

```gitignore
.env
__pycache__/
*.pyc
```

Add other local secrets or generated files when necessary.

## Agent Testing

Each provider should first be tested independently.

Example pattern:

```text
Provider API
    ↓
Provider client
    ↓
Simple test
    ↓
Successful response
    ↓
Main workflow integration
```

Do not integrate an untested provider into the main workflow.

## GitHub Workflow

The repository should be updated through normal Git commits.

Recommended sequence:

```text
Make change
 ↓
Run tests
 ↓
Review git diff/status
 ↓
Commit
 ↓
Push
```

Never use force-push to solve an ordinary branch synchronization problem.

## Human Approval

The system should require human approval for:
- major requirement changes
- production deployment
- destructive operations
- spending money
- publishing sensitive information
- changing authentication or security controls

## Current Integration Plan

```text
1. ChatGPT
2. Gemini
3. DeepSeek
4. Claude
5. Grok
6. Multi-agent orchestration
7. Automated testing
8. GitHub automation
9. Deployment automation
```

The order can change as the project develops.
