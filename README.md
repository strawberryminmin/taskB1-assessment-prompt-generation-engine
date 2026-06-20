# Prompt Engineering for Assessment Question Generation

This Python project compares prompt engineering strategies for generating assessment questions across domains and difficulty levels.

## Objective

The system accepts input such as:

```json
{
  "domain": "Python",
  "difficulty": "Easy"
}
```

It generates questions with three strategies:

- Basic Prompt
- Structured Prompt
- Role-Based Prompt

For each strategy, it creates Easy, Medium, and Hard questions for the selected domain, validates the output, prevents duplicates, and writes a comparison report.

## Project Structure

```text
project/
├── prompts/
│   └── prompt_library.py
├── generator/
│   └── question_generator.py
├── validation/
│   └── validator.py
├── reports/
│   ├── comparison_report.py
│   └── comparison_report.md
├── samples/
│   ├── generated_samples.json
│   ├── comparison_report.json
│   └── question_history.json
└── main.py
```

## Supported Domains

- Python
- Data Structures
- Database Management Systems
- Machine Learning

## How It Works

1. `prompts/prompt_library.py` stores all prompt templates and supported inputs.
2. `generator/question_generator.py` generates questions from strategy-specific question banks.
3. `validation/validator.py` rejects empty, off-topic, too-long, malformed, or difficulty-mismatched questions.
4. Duplicate detection is handled with `samples/question_history.json`.
5. `reports/comparison_report.py` scores strategies on relevance, clarity, difficulty control, and diversity.

## Run the Project

```bash
python main.py --input-json "{\"domain\":\"Python\",\"difficulty\":\"Easy\"}" --reset-history
```

You can also pass values directly:

```bash
python main.py --domain "Machine Learning" --difficulty "Hard" --reset-history
```

The command writes:

- `samples/generated_samples.json`
- `samples/comparison_report.json`
- `reports/comparison_report.md`

## Prompt Strategies

### Basic Prompt

A short direct prompt. It is fast and easy to maintain, but it gives the generator fewer constraints, so relevance and difficulty control may vary.

### Structured Prompt

A prompt with explicit domain, difficulty, format, and quality rules. It produces the most consistent output because it clearly defines what a valid question should look like.

### Role-Based Prompt

A prompt that asks the model to act like an experienced instructor. It tends to create clearer, more natural questions with good variety.

## Findings

Structured prompting performs best overall because it gives the strongest control over output format, topic relevance, and difficulty level. Role-Based prompting is close behind and is especially good for clarity and diversity. Basic prompting is useful for quick drafts, but it should be paired with validation before use in an assessment system.

## Sample Output

```json
{
  "strategy": "Role-Based",
  "domain": "Python",
  "difficulty": "Easy",
  "question": "What is a Python list?"
}
```
