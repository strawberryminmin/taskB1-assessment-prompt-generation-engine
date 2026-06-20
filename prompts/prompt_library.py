"""Prompt templates for assessment question generation."""

from __future__ import annotations

from dataclasses import dataclass
from string import Template


SUPPORTED_DOMAINS = (
    "Python",
    "Data Structures",
    "Database Management Systems",
    "Machine Learning",
)

SUPPORTED_DIFFICULTIES = ("Easy", "Medium", "Hard")


@dataclass(frozen=True)
class PromptStrategy:
    """Represents one prompt engineering strategy."""

    name: str
    description: str
    template: Template

    def render(self, domain: str, difficulty: str) -> str:
        return self.template.substitute(domain=domain, difficulty=difficulty)


PROMPT_STRATEGIES = {
    "Basic": PromptStrategy(
        name="Basic",
        description=(
            "A direct instruction prompt that asks for one assessment question "
            "with only minimal constraints."
        ),
        template=Template(
            "Generate one $difficulty assessment question for $domain. "
            "Return only the question text."
        ),
    ),
    "Structured": PromptStrategy(
        name="Structured",
        description=(
            "A constraint-heavy prompt that specifies domain, difficulty, "
            "format, length, and validation expectations."
        ),
        template=Template(
            "Create exactly one assessment question.\n"
            "Domain: $domain\n"
            "Difficulty: $difficulty\n"
            "Rules:\n"
            "- The question must test a concrete $domain concept.\n"
            "- The wording must be clear and concise.\n"
            "- The difficulty must match $difficulty learners.\n"
            "- Return only valid JSON with keys: question, domain, difficulty."
        ),
    ),
    "Role-Based": PromptStrategy(
        name="Role-Based",
        description=(
            "A persona prompt that asks the model to act as an expert assessment "
            "designer for the selected subject."
        ),
        template=Template(
            "You are an experienced $domain instructor and assessment designer. "
            "Write one $difficulty-level question that fairly evaluates a "
            "student's understanding of $domain. Keep it practical, unambiguous, "
            "and appropriate for the learner level. Return only the question."
        ),
    ),
}


def get_strategy_names() -> list[str]:
    """Return all available strategy names."""

    return list(PROMPT_STRATEGIES.keys())


def get_prompt(strategy: str, domain: str, difficulty: str) -> str:
    """Render a prompt for the requested strategy."""

    if strategy not in PROMPT_STRATEGIES:
        raise ValueError(f"Unknown prompt strategy: {strategy}")
    return PROMPT_STRATEGIES[strategy].render(domain=domain, difficulty=difficulty)
