import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from journal import log_event

load_dotenv()

PROJECT = "BRANHARD"
API_URL = "https://api.openai.com/v1/responses"
MODEL = "gpt-5.6-luna"


def save_file(folder, filename, content):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


def get_task():
    path = "project/tasks/current_task.md"

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ask_chatgpt(task):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "instructions": """
You are the BRANHARD AI Project Planner.

Your job is to turn a BRANHARD task into a clear,
professional implementation plan.

BRANHARD is a premium Nigerian streetwear brand.

Create:
1. Objective
2. Requirements
3. Design/UX requirements where relevant
4. Technical requirements where relevant
5. Step-by-step implementation plan
6. Testing checklist
7. Potential problems
8. Definition of done

Do not write the actual code unless it is necessary
to explain a technical requirement.
""",
        "input": task
    }

    response = requests.post(
        API_URL,
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
                text_parts.append(content.get("text", ""))

    result = "\n".join(text_parts).strip()

    if not result:
        raise RuntimeError("ChatGPT returned no text.")

    return result


def main():
    print("=" * 45)
    print("        BRANHARD AI WORKFLOW")
    print("=" * 45)

    task = input("\nWhat do you want the AI team to do?\n> ")

    if not task.strip():
        print("No task entered.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task_content = f"""# BRANHARD AI WORKFLOW TASK

Created: {timestamp}

## Task

{task}

## Workflow

1. ChatGPT — Plan
2. Claude — Build
3. Grok — Review
4. ChatGPT — Final decision
5. Claude — Apply fixes
6. Tests — Verify
7. GitHub — Save

## Status

CHATGPT PLANNING
"""

    save_file(
        "project/tasks",
        "current_task.md",
        task_content
    )

    print("\n✓ Task created")
log_event(
    "CHATGPT — PLAN",
    f"""### Task

{task}

### Plan File

{plan_file}

### Status

Plan completed. Next stage: CLAUDE — BUILD
"""
)
    print("✓ Sending task to ChatGPT...")

    try:
        plan = ask_chatgpt(task_content)
    except Exception as error:
        print("\n✗ ChatGPT error:")
        print(error)
        return

    plan_file = save_file(
        "project/requirements",
        "chatgpt_plan.md",
        f"""# BRANHARD — CHATGPT PROJECT PLAN

Generated: {timestamp}

## Original Task

{task}

## AI Plan

{plan}

## Next Agent

CLAUDE — BUILD
"""
    )

    print("\n✓ ChatGPT plan created")
    print(f"✓ Saved to: {plan_file}")

log_event(
    "CHATGPT — PLAN",
    f"""### Task

{task}

### Plan File

{plan_file}

### Status

Plan completed. Next stage: CLAUDE — BUILD
"""
)
    print("\nWORKFLOW STATUS")
    print("----------------")
    print("CHATGPT  ✓ PLAN")
    print("CLAUDE   → BUILD")
    print("GROK     → REVIEW")
    print("CHATGPT  → DECIDE")
    print("CLAUDE   → FIX")
    print("TEST     → VERIFY")
    print("GITHUB   → SAVE")


if __name__ == "__main__":
    main()

