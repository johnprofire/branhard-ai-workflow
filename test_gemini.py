from agents.gemini.client import create_agent

agent = create_agent("research")

result = agent.run(
    "Give me three useful ways an AI agent could help the BRANHARD clothing brand workflow.",
    system_prompt=(
        "You are the BRANHARD research and strategy agent. "
        "Give practical, concise and actionable recommendations."
    )
)

print("\nGEMINI RESPONSE")
print("=" * 50)
print(result)
