"""
Registry for AI agents.
"""

from app.ai.agents.base_agent import BaseAgent


class AgentRegistry:
    """
    Registry of available AI agents.
    """

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(
        self,
        agent: BaseAgent,
    ) -> None:
        self._agents[agent.name] = agent

    def get(
        self,
        name: str,
        ) -> BaseAgent:
            agent = self._agents.get(name)

            if agent is None:
                raise ValueError(
                    f"Unknown agent: {name}"
                )

            return agent

    def list(self) -> list[str]:
        return sorted(self._agents.keys())