"""Question generation engine with duplicate detection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from prompts.prompt_library import (
    SUPPORTED_DIFFICULTIES,
    SUPPORTED_DOMAINS,
    get_prompt,
    get_strategy_names,
)
from validation.validator import QuestionValidator


QUESTION_BANK = {
    "Basic": {
        "Python": {
            "Easy": [
                "What is a Python list?",
                "What is the purpose of a Python variable?",
            ],
            "Medium": [
                "Explain the difference between a Python list and a tuple?",
                "Why would you use a dictionary instead of a list in Python?",
            ],
            "Hard": [
                "Analyze how Python decorators can modify function behavior without changing the original function?",
                "Evaluate the trade-off between generators and lists when processing large Python datasets?",
            ],
        },
        "Data Structures": {
            "Easy": [
                "What is a stack data structure?",
                "What is the basic purpose of an array?",
            ],
            "Medium": [
                "Compare a stack and a queue in data structures?",
                "Explain why hash tables provide fast average-case lookup?",
            ],
            "Hard": [
                "Analyze the time complexity trade-off between adjacency lists and adjacency matrices for graph storage?",
                "Design a data structure that supports insert, delete, and random access efficiently?",
            ],
        },
        "Database Management Systems": {
            "Easy": [
                "What is a table in a database?",
                "What is the purpose of a primary key in a database?",
            ],
            "Medium": [
                "Explain the difference between an INNER JOIN and a LEFT JOIN in SQL?",
                "Why is normalization used when designing a database schema?",
            ],
            "Hard": [
                "Analyze how database indexing can improve reads while slowing down writes?",
                "Evaluate the trade-off between normalization and denormalization in database design?",
            ],
        },
        "Machine Learning": {
            "Easy": [
                "What is a training dataset in machine learning?",
                "What is the basic purpose of a machine learning model?",
            ],
            "Medium": [
                "Explain the difference between classification and regression in machine learning?",
                "Why is validation data used during machine learning model development?",
            ],
            "Hard": [
                "Analyze how overfitting affects a machine learning model's performance on unseen data?",
                "Design a machine learning evaluation plan for an imbalanced classification dataset?",
            ],
        },
    },
    "Structured": {
        "Python": {
            "Easy": [
                "What is the purpose of the print function in Python?",
                "Identify the Python data type used to store key-value pairs?",
            ],
            "Medium": [
                "Compare Python lists and dictionaries for storing searchable data?",
                "Explain why exception handling is useful in Python programs?",
            ],
            "Hard": [
                "Design a Python class structure for representing students, courses, and enrollments?",
                "Analyze the complexity trade-off of using a set instead of a list for membership checks in Python?",
            ],
        },
        "Data Structures": {
            "Easy": [
                "What is the basic purpose of a queue data structure?",
                "Identify the data structure that follows last-in, first-out behavior?",
            ],
            "Medium": [
                "Explain why a binary search tree can make searching faster than a linked list?",
                "Compare breadth-first traversal and depth-first traversal in a tree?",
            ],
            "Hard": [
                "Design a graph traversal approach to detect cycles in a directed graph?",
                "Analyze the complexity trade-off between a binary heap and a sorted array for priority queue operations?",
            ],
        },
        "Database Management Systems": {
            "Easy": [
                "What is the purpose of a foreign key in a database?",
                "Identify the SQL command used to retrieve rows from a table?",
            ],
            "Medium": [
                "Explain why transactions are important in database management systems?",
                "Compare clustered and non-clustered database indexes?",
            ],
            "Hard": [
                "Design a normalized database schema for orders, customers, and products?",
                "Analyze how ACID properties protect database consistency during concurrent transactions?",
            ],
        },
        "Machine Learning": {
            "Easy": [
                "What is a feature in machine learning?",
                "Identify the machine learning task used to predict categories?",
            ],
            "Medium": [
                "Explain why splitting data into training and validation sets improves machine learning evaluation?",
                "Compare supervised and unsupervised learning in machine learning?",
            ],
            "Hard": [
                "Design a machine learning pipeline that reduces data leakage during model evaluation?",
                "Analyze the trade-off between bias and variance in a machine learning model?",
            ],
        },
    },
    "Role-Based": {
        "Python": {
            "Easy": [
                "What is a Python list?",
                "What is the basic purpose of a loop in Python?",
                "What is a Python dictionary and when would you use it?",
                "How do you create and call a function in Python?",
                "What is the difference between a string and a list in Python?",
                "What does the range function do in Python?",
                "How do you add an item to a Python list?",
            ],
            "Medium": [
                "Explain why Python functions help make code reusable?",
                "Compare local and global variables in Python?",
            ],
            "Hard": [
                "Design a Python generator-based solution for reading a large file without loading it fully into memory?",
                "Evaluate the trade-off between inheritance and composition when designing Python classes?",
            ],
        },
        "Data Structures": {
            "Easy": [
                "What is a linked list in data structures?",
                "What is the basic purpose of a tree data structure?",
            ],
            "Medium": [
                "Explain why a queue is suitable for breadth-first traversal of a graph?",
                "Compare arrays and linked lists for insertion operations?",
            ],
            "Hard": [
                "Design a balanced tree strategy to keep search operations efficient after repeated insertions?",
                "Analyze the complexity trade-off of using a hash table for duplicate detection in a large dataset?",
            ],
        },
        "Database Management Systems": {
            "Easy": [
                "What is SQL used for in a database management system?",
                "What is the basic purpose of a database schema?",
            ],
            "Medium": [
                "Explain why a database index can speed up search queries?",
                "Compare primary keys and foreign keys in database tables?",
            ],
            "Hard": [
                "Design a transaction strategy that prevents lost updates in a database management system?",
                "Evaluate the trade-off between strong consistency and availability in distributed databases?",
            ],
        },
        "Machine Learning": {
            "Easy": [
                "What is supervised learning in machine learning?",
                "What is the basic purpose of model training in machine learning?",
            ],
            "Medium": [
                "Explain why overfitting is a problem in machine learning?",
                "Compare precision and recall for a machine learning classifier?",
            ],
            "Hard": [
                "Design a machine learning strategy for improving recall without causing too many false positives?",
                "Analyze how regularization helps control overfitting in machine learning models?",
            ],
        },
    },
}


class QuestionGenerator:
    """Generates questions for all strategies while avoiding duplicates."""

    def __init__(self, history_path: str | Path = "samples/question_history.json") -> None:
        self.history_path = Path(history_path)
        self.validator = QuestionValidator()
        self.history = self._load_history()

    def generate(self, domain: str, difficulty: str, strategy: str) -> dict[str, str]:
        self._validate_inputs(domain, difficulty, strategy)

        for question in self._candidate_questions(strategy, domain, difficulty):
            normalized = self._normalize(question)
            is_valid, errors = self.validator.validate(question, domain, difficulty)
            if normalized not in self.history and is_valid:
                self.history.add(normalized)
                self._save_history()
                return {
                    "strategy": strategy,
                    "domain": domain,
                    "difficulty": difficulty,
                    "question": question,
                    "prompt": get_prompt(strategy, domain, difficulty),
                }
            if errors:
                continue

        raise RuntimeError(
            f"No valid non-duplicate question available for {strategy}, {domain}, {difficulty}"
        )

    def generate_all(
        self,
        domain: str,
        difficulties: Iterable[str] = SUPPORTED_DIFFICULTIES,
        strategies: Iterable[str] | None = None,
    ) -> list[dict[str, str]]:
        strategy_names = list(strategies or get_strategy_names())
        return [
            self.generate(domain=domain, difficulty=difficulty, strategy=strategy)
            for strategy in strategy_names
            for difficulty in difficulties
        ]

    def reset_history(self) -> None:
        self.history.clear()
        self._save_history()

    def _candidate_questions(self, strategy: str, domain: str, difficulty: str) -> list[str]:
        return QUESTION_BANK[strategy][domain][difficulty]

    def _validate_inputs(self, domain: str, difficulty: str, strategy: str) -> None:
        if domain not in SUPPORTED_DOMAINS:
            raise ValueError(f"Unsupported domain: {domain}")
        if difficulty not in SUPPORTED_DIFFICULTIES:
            raise ValueError(f"Unsupported difficulty: {difficulty}")
        if strategy not in get_strategy_names():
            raise ValueError(f"Unsupported strategy: {strategy}")

    def _load_history(self) -> set[str]:
        if not self.history_path.exists():
            return set()
        with self.history_path.open("r", encoding="utf-8") as file:
            return set(json.load(file))

    def _save_history(self) -> None:
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with self.history_path.open("w", encoding="utf-8") as file:
            json.dump(sorted(self.history), file, indent=2)

    @staticmethod
    def _normalize(question: str) -> str:
        return " ".join(question.lower().strip().split())
