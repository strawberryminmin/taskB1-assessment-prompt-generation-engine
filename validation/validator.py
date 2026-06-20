"""Validation rules for generated assessment questions."""

from __future__ import annotations

from prompts.prompt_library import SUPPORTED_DIFFICULTIES, SUPPORTED_DOMAINS


DOMAIN_KEYWORDS = {
    "Python": {
        "python",
        "list",
        "tuple",
        "dictionary",
        "function",
        "class",
        "decorator",
        "generator",
        "exception",
        "loop",
    },
    "Data Structures": {
        "array",
        "stack",
        "queue",
        "tree",
        "graph",
        "hash",
        "heap",
        "linked list",
        "complexity",
        "traversal",
    },
    "Database Management Systems": {
        "database",
        "sql",
        "table",
        "transaction",
        "normalization",
        "index",
        "join",
        "key",
        "acid",
        "schema",
    },
    "Machine Learning": {
        "model",
        "training",
        "feature",
        "classification",
        "regression",
        "overfitting",
        "gradient",
        "dataset",
        "validation",
        "learning",
    },
}


DIFFICULTY_SIGNALS = {
    "Easy": {"define", "what", "identify", "basic", "simple", "purpose"},
    "Medium": {"explain", "compare", "difference", "implement", "choose", "why"},
    "Hard": {"design", "analyze", "optimize", "evaluate", "trade-off", "complexity"},
}


class QuestionValidator:
    """Validates generated questions against project quality gates."""

    def __init__(self, max_length: int = 220) -> None:
        self.max_length = max_length

    def validate(self, question: str, domain: str, difficulty: str) -> tuple[bool, list[str]]:
        errors: list[str] = []
        normalized_question = question.strip()

        if domain not in SUPPORTED_DOMAINS:
            errors.append(f"Unsupported domain: {domain}")

        if difficulty not in SUPPORTED_DIFFICULTIES:
            errors.append(f"Unsupported difficulty: {difficulty}")

        if not normalized_question:
            errors.append("Question is empty")
            return False, errors

        if len(normalized_question) > self.max_length:
            errors.append("Question is excessively long")

        if not normalized_question.endswith("?"):
            errors.append("Question must end with a question mark")

        if domain in DOMAIN_KEYWORDS and not self._contains_domain_keyword(normalized_question, domain):
            errors.append("Question does not appear to belong to the selected domain")

        if difficulty in DIFFICULTY_SIGNALS and not self._matches_difficulty(normalized_question, difficulty):
            errors.append("Question may be irrelevant to the requested difficulty")

        return not errors, errors

    def _contains_domain_keyword(self, question: str, domain: str) -> bool:
        text = question.lower()
        return any(keyword in text for keyword in DOMAIN_KEYWORDS[domain])

    def _matches_difficulty(self, question: str, difficulty: str) -> bool:
        text = question.lower()
        signals = DIFFICULTY_SIGNALS[difficulty]
        return any(signal in text for signal in signals)
