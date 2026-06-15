import ast
from typing import Optional

from schemas.schemas import CustomResponse


def extract_function_signature(code: str) -> Optional[tuple[str, list[str]]]:
    """
    Extract function name and parameter names from Python code.
    Returns (function_name, param_names) or None if no function found.
    """
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "solution":
                param_names = [arg.arg for arg in node.args.args]
                return ("solution", param_names)
        return None
    except SyntaxError:
        return None


def validate_parameters(code: str, expected_params: list[str]) -> CustomResponse:
    """
    Validate that function parameters match expected parameter names.
    Returns a CustomResponse object with success state and an error message if there are any errors.
    """
    result = extract_function_signature(code)

    if result is None:
        return CustomResponse(
            success=False, error="Could not find 'solution' function in your code."
        )

    _, actual_params = result

    if actual_params != expected_params:
        return CustomResponse(
            success=False,
            error=f"Expected parameters: {', '.join(expected_params)}, but got: {', '.join(actual_params)}",
        )

    return CustomResponse(success=True)
