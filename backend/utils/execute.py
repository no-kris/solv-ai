import json
import sys
from typing import Annotated

from schemas.schemas import (
    GenericTestCase,
    GraphTestCase,
    LinkedListTestCase,
    TreeTestCase,
)

TestCase = Annotated[
    GenericTestCase | TreeTestCase | LinkedListTestCase | GraphTestCase,
    "TestCase",
]


def execute_user_code(
    code: str,
    tests: list[TestCase],
    param_names: list[str],
) -> dict:
    """Execute user code against test cases."""
    namespace = {}
    try:
        exec(code, namespace)
        solution = namespace.get("solution")
        if solution is None:
            return {"success": False, "error": "solution function not found"}
    except SyntaxError as e:
        return {"success": False, "error": f"Syntax error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Error loading code: {str(e)}"}

    passed = 0

    for test in tests:
        try:
            args = build_test_args(test, param_names)
            result = solution(*args)
            if result == test.expectedOutput:
                passed += 1
        except Exception as e:
            print(f"Test exception: {type(e).__name__}: {str(e)}", file=sys.stderr)

    return {"success": True, "passed": passed, "total": len(tests)}


def build_test_args(test: TestCase, param_names: list[str]) -> tuple:
    """Build function arguments from test case based on type."""
    args = []

    if isinstance(test, LinkedListTestCase):
        for param_name in param_names:
            if param_name == "head":
                args.append(test.head)
            else:
                args.append(test.params.get(param_name))
    elif isinstance(test, TreeTestCase):
        for param_name in param_names:
            if param_name == "root":
                args.append(test.root)
            else:
                args.append(test.params.get(param_name))
    elif isinstance(test, GraphTestCase):
        for param_name in param_names:
            if param_name == "edges":
                args.append(test.edges)
            elif param_name == "start" or param_name == "node":
                args.append(test.start)
            elif param_name == "target":
                args.append(test.target)
            else:
                args.append(test.params.get(param_name))
    elif isinstance(test, GenericTestCase):
        for param_name in param_names:
            args.append(test.params.get(param_name))

    return tuple(args)


if __name__ == "__main__":
    tests_data = json.loads(sys.argv[1])
    param_names = json.loads(sys.argv[2])
    code = sys.argv[3]

    # Parse JSON dicts into Pydantic models
    tests = []
    for test in tests_data:
        if test.get("type") == "generic":
            tests.append(GenericTestCase(**test))
        elif test.get("type") == "tree":
            tests.append(TreeTestCase(**test))
        elif test.get("type") == "linked_list":
            tests.append(LinkedListTestCase(**test))
        elif test.get("type") == "graph":
            tests.append(GraphTestCase(**test))

    result = execute_user_code(code, tests, param_names)
    print(json.dumps(result))
