import os
from datetime import datetime

JOURNAL = "project/journal/BRANHARD_AI_JOURNAL.md"


def log_event(stage, content):
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""

---

## {stage}

**Date:** {timestamp}

{content}

"""

    with open(JOURNAL, "a", encoding="utf-8") as file:
        file.write(entry)

    print(f"✓ Journal updated: {stage}")


if __name__ == "__main__":
    log_event(
        "SYSTEM TEST",
        "Automatic BRANHARD AI journal logging is working."
    )
