import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("project/workflow_state.json")

STAGES = [
    "TASK_CREATED",
    "CHATGPT_PLAN",
    "CLAUDE_BUILD",
    "GROK_REVIEW",
    "CHATGPT_DECIDE",
    "CLAUDE_FIX",
    "TEST_VERIFY",
    "GITHUB_SAVE",
    "COMPLETE",
]

OWNERS = {
    "TASK_CREATED": "SYSTEM",
    "CHATGPT_PLAN": "CHATGPT",
    "CLAUDE_BUILD": "CLAUDE",
    "GROK_REVIEW": "GROK",
    "CHATGPT_DECIDE": "CHATGPT",
    "CLAUDE_FIX": "CLAUDE",
    "TEST_VERIFY": "TEST",
    "GITHUB_SAVE": "GITHUB",
    "COMPLETE": "SYSTEM",
}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def load_state():
    if not STATE_FILE.exists():
        return {
            "status": "NOT_STARTED",
            "sequence": 0,
            "history": []
        }

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)

def start_stage(stage):
    if stage not in STAGES:
        raise ValueError(f"Unknown stage: {stage}")

    state = load_state()
    current = state["status"]

    if current != "NOT_STARTED":
        if current == "COMPLETE":
            raise ValueError("Workflow is already complete.")

        current_index = STAGES.index(current)
        requested_index = STAGES.index(stage)

        if requested_index != current_index + 1:
            raise ValueError(
                f"Invalid transition: {current} → {stage}"
            )

    state["sequence"] += 1
    state["status"] = stage

    event = {
        "sequence": state["sequence"],
        "stage": stage,
        "owner": OWNERS[stage],
        "status": "STARTED",
        "timestamp_utc": utc_now()
    }

    state["history"].append(event)
    save_state(state)

    print(f"✓ Stage started: {stage}")
    print(f"  Owner: {OWNERS[stage]}")
    print(f"  Sequence: {state['sequence']}")

    return state



def complete_stage(stage, result="SUCCESS"):
    state = load_state()

    if state["status"] != stage:
        raise ValueError(
            f"Cannot complete {stage}. "
            f"Current stage is {state['status']}."
        )

    state["history"][-1]["status"] = result
    state["history"][-1]["completed_at_utc"] = utc_now()

    save_state(state)

    print(f"✓ Stage completed: {stage} → {result}")

def show_state():
    state = load_state()

    print("\nBRANHARD WORKFLOW STATE")
    print("=" * 40)
    print(f"Current stage: {state['status']}")
    print(f"Sequence:      {state['sequence']}")
    print(f"Events:        {len(state['history'])}")

    if state["history"]:
        print("\nHistory:")

        for event in state["history"]:
            print(
                f"{event['sequence']}. "
                f"{event['stage']} — "
                f"{event['status']} — "
                f"{event['owner']}"
            )

if __name__ == "__main__":
    print("BRANHARD Stage Controller")
    print("=" * 40)

    state = load_state()

    if state["status"] == "NOT_STARTED":
        start_stage("TASK_CREATED")
        complete_stage("TASK_CREATED")

    show_state()

