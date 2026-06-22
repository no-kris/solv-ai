import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from schemas.schemas import (
    CustomResponse,
    GenericTestCase,
    GraphTestCase,
    LinkedListTestCase,
    TreeTestCase,
    ValidationResponse,
)

TestCase = Annotated[
    GenericTestCase | TreeTestCase | LinkedListTestCase | GraphTestCase,
    "TestCase",
]


_env = os.environ.copy()
for key in ("HF_TOKEN", "MODEL", "ALLOWED_ORIGINS"):
    _env.pop(key, None)


def execute_code(
    code: str, tests: list[TestCase], param_names: list[str]
) -> ValidationResponse | CustomResponse:
    """
    Run a subprocess on the users code.
    """
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(__file__),
                json.dumps([t.model_dump() for t in tests]),  # argv[1]
                json.dumps(param_names),  # argv[2]
                code,
            ],
            capture_output=True,
            text=True,
            timeout=30,
            env=_env,
        )
    except subprocess.TimeoutExpired:
        return CustomResponse(
            success=False, error="Code execution timed out (infinite loop?)"
        )
    except Exception as e:
        return CustomResponse(success=False, error=f"Execution error: {str(e)}")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        return CustomResponse(
            success=False,
            error=stderr or f"Process exited with code {result.returncode}",
        )

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        return CustomResponse(
            success=False,
            error="Failed to parse execution output",
        )

    if not output.get("success", False):
        return CustomResponse(success=False, error=output.get("error", "Unknown error"))

    return ValidationResponse(passed=output["passed"], total=len(tests))


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
