from typing import Any, Optional

from pydantic import BaseModel


class GenerateProblemRequest(BaseModel):
    category: str
    difficulty: str


class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: str


class TestCase(BaseModel):
    params: dict[str, Any]
    expectedOutput: Any


class NodeField(BaseModel):
    name: str
    default: str


class NodeStructure(BaseModel):
    className: str
    fields: list[NodeField]


class CodingProblem(BaseModel):
    isSet: bool = True
    description: str
    paramNames: list[str]
    examples: list[ProblemExample]
    tests: list[TestCase]
    nodeStructure: Optional[NodeStructure] = None


class CustomResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    content: Optional[CodingProblem] = None
