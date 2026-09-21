import subprocess
from datetime import datetime
from pathlib import Path

JOURNAL = Path("project/journal/BRANHARD_AI_JOURNAL.md")


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Git error:")
        print(result.stderr)
        return False

    return True


def journal_event(stage, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    JOURNAL.parent.mkdir(parents=True, exist_ok=True)

    with open(JOURNAL, "a", encoding="utf-8") as file:
        file.write(
            f"\n### {stage}\n"
            f"**Time:** {timestamp}\n\n"
            f"{message}\n\n"
        )

    print(f"✓ Journal updated: {stage}")

    # Only stage the journal — nothing else.
    if not run_command(
        "git add project/journal/BRANHARD_AI_JOURNAL.md"
    ):
        return False

    commit_message = f"Update AI journal: {stage}"

    if not run_command(
        f'git commit -m "{commit_message}"'
    ):
        return False

    if not run_command("git push"):
        return False

    print("✓ Journal pushed to GitHub")
    return True


if __name__ == "__main__":
    journal_event(
        "AUTOMATION TEST",
        "Automatic journal-to-GitHub system successfully tested."
    )
