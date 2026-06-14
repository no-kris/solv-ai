import json
from typing import Optional

from schemas.schemas import (
    CodingProblem,
    GenericTestCase,
    GraphTestCase,
    LinkedListTestCase,
    NodeField,
    NodeStructure,
    TreeTestCase,
)


def get_test_case_class(category: str):
    """
    Return the correct test case schema to use based on the coding problem category (i.e Linked List, Trees, Graphs)
    """
    match category:
        case "Linked Lists":
            return LinkedListTestCase
        case "Trees":
            return TreeTestCase
        case "Graphs":
            return GraphTestCase
        case _:
            return GenericTestCase


def get_node_structure(category: str) -> Optional[NodeStructure]:
    """
    Construct and return the NodeStructure for any coding problem categorie (i.e Linked List, Trees, Graphs) that utilize a node data structure.
    """
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


def strip_llm_markdown_formatting(content_str: str) -> str:
    """
    Strip the garbage that the llm sometimes appends to the output. (i.e. the ```json ... ``` stuff)
    """
    content_str_cpy = content_str
    if content_str_cpy.startswith("```"):
        content_str_cpy = content_str_cpy.split("```")[1]
    if content_str_cpy.startswith("json"):
        content_str_cpy = content_str_cpy[4:]
    if content_str_cpy.endswith("```"):
        content_str_cpy = content_str_cpy[:-3]
    return content_str_cpy


def structure_problem_data(
    problem_data: Optional[str], category: str
) -> Optional[CodingProblem]:
    """
    Make sure the coding problem follows the structure associated in the pydantic schema.
    Returns none if there is no problem data.
    """
    if not problem_data:
        return None

    problem_json = json.loads(problem_data)

    test_case_class = get_test_case_class(category)
    problem_json["tests"] = [
        test_case_class(**test) for test in problem_json.get("tests", [])
    ]

    problem = CodingProblem(**problem_json)
    problem.nodeStructure = get_node_structure(category)
    return problem
