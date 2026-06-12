import json

from schemas.schemas import CodingProblem, NodeField, NodeStructure


def get_node_structure(category: str) -> NodeStructure | None:
    match category:
        case "Linked Lists":
            return NodeStructure(
                className="ListNode",
                fields=[
                    NodeField(name="val", default="0"),
                    NodeField(name="next", default="None"),
                ],
            )
        case "Trees":
            return NodeStructure(
                className="TreeNode",
                fields=[
                    NodeField(name="val", default="0"),
                    NodeField(name="left", default="None"),
                    NodeField(name="right", default="None"),
                ],
            )
        case "Graphs":
            return NodeStructure(
                className="GraphNode",
                fields=[
                    NodeField(name="val", default="0"),
                    NodeField(name="neighbors", default="None"),
                ],
            )
        case _:
            return None


def render_node_class(node: NodeStructure) -> str:
    params = ", ".join(f"{f.name}={f.default}" for f in node.fields)
    body = "\n".join(f"\tself.{f.name} = {f.name}" for f in node.fields)
    return f"class {node.className}:\n\tdef __init__(self, {params}):\n{body}"


def build_prompt(category: str, difficulty: str) -> str:
    schema = CodingProblem.model_json_schema()

    schema_str = json.dumps(schema, indent=2)

    node = get_node_structure(category)
    node_section = ""
    if node is not None:
        node_section = f"""
This problem uses the following data structure. Assume it is already defined, and write all examples and test cases against it:
{render_node_class(node)}
"""

    return f"""You are an expert coding interview question generator. Generate a {difficulty} level {category} problem.

Return a JSON object STRICTLY matching this schema:
{schema_str}
{node_section}
Requirements:
- Description: Clear, concise problem statement (2-3 sentences)
- paramNames: Use realistic, descriptive names (e.g., "nums", "target", "k")
- examples: Include 2-3 examples with clear explanations
- tests: Include 3-5 edge case and normal test cases

Generate the problem now:"""
