from agents.deepseek.client import create_agent

agent = create_agent("research")

result = agent.run(
    "Give me three useful things an AI agent could do for the BRANHARD clothing brand workflow.",
    system_prompt=(
        "You are the BRANHARD AI research and analysis agent. "
        "Be practical, concise, and identify useful actionable ideas."
    )
)

print("\nDEEPSEEK RESPONSE")
print("=" * 50)
print(result)
