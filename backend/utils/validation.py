import ast
from typing import Optional

from schemas.schemas import CustomResponse

BLOCKED_IMPORTS = {
    "os",
    "subprocess",
    "sys",
    "socket",
    "requests",
    "pathlib",
    "shutil",
    "ctypes",
    "builtins",
    "importlib",
    "inspect",
    "ast",
    "pickle",
    "marshal",
    "shelve",
    "sqlite3",
    "multiprocessing",
    "threading",
    "signal",
    "mmap",
    "resource",
}

BLOCKED_BUILTINS = {
    "open",
    "exec",
    "eval",
    "compile",
    "__import__",
    "breakpoint",
    "input",
}


def has_dangerous_imports(code: str) -> CustomResponse:
    """
    Check for dangerous imports and function calls. (i.e any imports/functions that attempt to access the os, files, or network.)
    """

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in BLOCKED_IMPORTS:
                        return CustomResponse(
                            success=True, error=f"Import '{alias.name}' is not allowed."
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module in BLOCKED_IMPORTS:
                    return CustomResponse(
                        success=True,
                        error=f"Import from '{node.module}' is not allowed.",
                    )
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_BUILTINS:
                    return CustomResponse(
                        success=True,
                        error=f"Calling '{node.func.id}' is not allowed.",
                    )
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr in BLOCKED_BUILTINS
                ):
                    return CustomResponse(
                        success=True,
                        error=f"Calling '{node.func.attr}' is not allowed.",
                    )
        return CustomResponse(success=False)
    except SyntaxError:
        return CustomResponse(success=False)


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
        return CustomResponse(success=False, error="You're code has errors.")

    _, actual_params = result

    if actual_params != expected_params:
        return CustomResponse(
            success=False,
            error=f"Expected parameters: {', '.join(expected_params)}, but got: {', '.join(actual_params)}",
        )

    return CustomResponse(success=True)
