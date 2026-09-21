
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from github_journal import journal_event

# Load API keys from .env
load_dotenv()

PROJECT = "BRANHARD"
OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.6-luna"

TASK_FILE = "project/tasks/current_task.md"
PLAN_FILE = "project/requirements/chatgpt_plan.md"
JOURNAL_FILE = "project/journal/BRANHARD_AI_JOURNAL.md"


# ============================================================
# FILE FUNCTIONS
# ============================================================

def save_file(path, content):
    folder = os.path.dirname(path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return path


def append_journal(stage, content):
    os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""

---

## {stage}

**Date:** {timestamp}

{content}

"""

    with open(JOURNAL_FILE, "a", encoding="utf-8") as file:
        file.write(entry)

    print(f"✓ Journal updated: {stage}")


# ============================================================
# CHATGPT
# ============================================================

def ask_chatgpt(task):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing from .env"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENAI_MODEL,

        "instructions": """
You are the BRANHARD AI Project Planner.

BRANHARD is a premium Nigerian streetwear brand.

Your job is to turn the user's task into a clear,
professional implementation plan.

Create the following sections:

1. Objective
2. Requirements
3. Design and UX requirements
4. Technical requirements
5. Step-by-step implementation plan
6. Testing checklist
7. Potential problems
8. Definition of done

Do not write the actual implementation code unless
code is necessary to explain a technical requirement.

Be practical, specific and organized.
""",

        "input": task
    }

    response = requests.post(
        OPENAI_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenAI API error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    text_parts = []

    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(
                    content.get("text", "")
                )

    result = "\n".join(text_parts).strip()

    if not result:
        raise RuntimeError(
            "ChatGPT returned no text."
        )

    return result


# ============================================================
# CREATE TASK
# ============================================================

def create_task(task):
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    task_content = f"""# BRANHARD AI WORKFLOW TASK

Created: {timestamp}

## Task

{task}

## Workflow

1. ChatGPT — PLAN
2. Claude — BUILD
3. Grok — REVIEW
4. ChatGPT — DECIDE
5. Claude — FIX
6. TEST — VERIFY
7. GitHub — SAVE
8. Journal — RECORD

## Status

CHATGPT PLANNING
"""

    save_file(TASK_FILE, task_content)

    append_journal(
        "TASK CREATED",
        f"""### Task

{task}

### Status

CHATGPT PLANNING
"""
    )


# ============================================================
# MAIN WORKFLOW
# ============================================================

def main():

    print("=" * 55)
    print("              BRANHARD AI WORKFLOW")
    print("=" * 55)

    print("""
AI TEAM

ChatGPT  → PLAN
Claude   → BUILD
Grok     → REVIEW
ChatGPT  → DECIDE
Claude   → FIX
TEST     → VERIFY
GitHub   → SAVE
Journal  → RECORD
""")

    task = input(
        "What do you want the AI team to do?\n> "
    ).strip()

    if not task:
        print("\nNo task entered.")
        return

    # --------------------------------------------------------
    # TASK
    # --------------------------------------------------------

    print("\nCreating task...")

    create_task(task)

    print("\n✓ Task created")
    print(f"✓ Saved to: {TASK_FILE}")

    # --------------------------------------------------------
    # CHATGPT PLAN
    # --------------------------------------------------------

    print("\nSending task to ChatGPT...")

    append_journal(
        "CHATGPT — STARTED",
        f"""ChatGPT has started planning the following task:

{task}
"""
    )

    try:
        plan = ask_chatgpt(
            open(TASK_FILE, encoding="utf-8").read()
        )

    except Exception as error:

        print("\n✗ ChatGPT error:")
        print(error)

        append_journal(
            "CHATGPT — ERROR",
            f"""### Error

{error}

### Status

CHATGPT PLANNING FAILED
"""
        )

        return

    # --------------------------------------------------------
    # SAVE PLAN
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    plan_content = f"""# BRANHARD — CHATGPT PROJECT PLAN

Generated: {timestamp}

## Original Task

{task}

## AI PLAN

{plan}

## Next Agent

CLAUDE — BUILD
"""

    save_file(
        PLAN_FILE,
        plan_content
    )

    print("\n✓ ChatGPT plan created")
    print(f"✓ Saved to: {PLAN_FILE}")

    # --------------------------------------------------------
    # JOURNAL PLAN
    # --------------------------------------------------------

    append_journal(
        "CHATGPT — PLAN",
        f"""### Task

{task}

### Plan

{plan}

### Plan File

{PLAN_FILE}

### Next Stage

CLAUDE — BUILD
"""
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print("\n")
    print("=" * 55)
    print("              WORKFLOW STATUS")
    print("=" * 55)

    print("""
CHATGPT  ✓ PLAN
CLAUDE   → BUILD
GROK     → REVIEW
CHATGPT  → DECIDE
CLAUDE   → FIX
TEST     → VERIFY
GITHUB   → SAVE
JOURNAL  ✓ RECORD
""")

    journal_event(
        "TASK CREATED",
        f"Task created successfully:\n\n{task}"
    )

    journal_event(
        "TASK CREATED",
        f"Task created successfully:\n\n{task}"
    )

    print("=" * 55)
    print("Task successfully recorded.")
    print("=" * 55)

# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
