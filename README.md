# BRANHARD AI WORKFLOW

A multi-agent AI workflow for planning, research, development, review, testing, version control, and documentation for the BRANHARD project.

## Purpose

The system is designed so different AI agents can specialize in different jobs while GitHub remains the project source of truth and the workflow journal records important events.

## AI Team

| Agent | Primary role | Current status |
|---|---|---|
| ChatGPT | Planning, orchestration, decisions | Connected |
| Gemini | Research and alternative analysis | Connected |
| DeepSeek | Research and analysis | API access/credit pending |
| Claude | Coding and implementation | Pending |
| Grok | Independent review and research | Pending |

## Planned Workflow

```text
YOU
 ↓
CHATGPT — PLAN
 ↓
RESEARCH / ANALYSIS
 ├── GEMINI
 ├── DEEPSEEK
 └── GROK
 ↓
CHATGPT — DECIDE
 ↓
CLAUDE — BUILD
 ↓
CLAUDE — FIX
 ↓
TEST — VERIFY
 ↓
GITHUB — SAVE
 ↓
JOURNAL — RECORD
```

## Project Structure

```text
branhard-ai-workflow/
├── agents/
│   ├── chatgpt/
│   ├── claude/
│   ├── deepseek/
│   ├── gemini/
│   └── grok/
├── workflows/
│   ├── plan/
│   ├── build/
│   ├── review/
│   └── deploy/
├── project/
│   ├── requirements/
│   ├── tasks/
│   ├── reviews/
│   ├── reports/
│   ├── journal/
│   └── decisions/
├── tests/
├── workflow.py
├── stage_controller.py
├── github_journal.py
├── journal.py
├── config.json
├── README.md
└── .env
```

## Security

API keys and other secrets must never be committed to GitHub.

Secrets belong in the local `.env` file. The `.env` file should remain excluded by `.gitignore`.

Never place API keys in:
- source code
- README files
- journal entries
- screenshots
- GitHub issues or commits
- shared documents

## Current Progress

### Completed

- Python workflow foundation
- ChatGPT API connection
- Gemini API connection
- GitHub repository
- SSH authentication
- Workflow journal
- Journal automation
- Stage controller

### Pending

- DeepSeek API access/credit
- Claude API setup
- Grok API setup
- Full multi-agent orchestration
- Automatic agent handoffs
- Automated testing pipeline
- Final deployment workflow

## Development Rules

1. Never expose API keys or secrets.
2. Never use `git push --force`.
3. Keep `.env` out of GitHub.
4. Test each AI independently before integrating it into the main workflow.
5. Keep GitHub as the source of truth for project code.
6. Record important workflow events in the journal.
7. Use the stage controller to prevent invalid workflow transitions.
8. Do not silently change major project requirements.
9. Test changes before marking a task complete.

## Long-Term Goal

Create a reliable multi-agent system that can take a BRANHARD task through:

```text
Idea
 ↓
Planning
 ↓
Research
 ↓
Implementation
 ↓
Review
 ↓
Decision
 ↓
Fixes
 ↓
Testing
 ↓
GitHub
 ↓
Deployment
```

while maintaining a clear project history and journal.
