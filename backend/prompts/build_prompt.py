import json

from schemas.schemas import CodingProblem


def build_prompt(category: str, difficulty: str) -> str:
    schema = CodingProblem.model_json_schema()
    schema_str = json.dumps(schema, indent=2)

    return f"""You are an expert coding interview question generator. Generate a {difficulty} level {category} problem.

Return a JSON object STRICTLY matching this schema:
{schema_str}

Requirements:
- Description: Clear, concise problem statement (2-3 sentences)
- paramNames: Use realistic, descriptive names (e.g., "nums", "target", "k")
- examples: Include 2-3 examples with clear explanations
- tests: Include 3-5 edge case and normal test cases

Generate the problem now:"""
