from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, Discriminator


class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: str


class NodeField(BaseModel):
    name: str
    default: str


class NodeStructure(BaseModel):
    className: str
    fields: list[NodeField]


class GenericTestCase(BaseModel):
    type: Literal["generic"]
    params: dict[str, Any]
    expectedOutput: Any


class TreeTestCase(BaseModel):
    type: Literal["tree"]
    root: Optional[dict[str, Any]] = None
    expectedOutput: Any


class LinkedListTestCase(BaseModel):
    type: Literal["linked_list"]
    head: Optional[dict[str, Any]] = None
    expectedOutput: Any


class GraphTestCase(BaseModel):
    type: Literal["graph"]
    start: str
    target: str
    edges: dict[str, list[Any]]
    expectedOutput: Any


class CodingProblem(BaseModel):
    isSet: bool = True
    description: str
    paramNames: list[str]
    examples: list[ProblemExample]
    tests: list[
        Annotated[
            GenericTestCase | TreeTestCase | LinkedListTestCase | GraphTestCase,
            Discriminator("type"),
        ]
    ]
    nodeStructure: Optional[NodeStructure] = None


class CustomResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    content: Optional[str] = None


class ValidationResponse(BaseModel):
    passed: int
    total: int


class GenerateProblemRequest(BaseModel):
    category: str
    difficulty: str


class ValidateProblemRequest(BaseModel):
    code: str
    tests: list[
        Annotated[
            GenericTestCase | TreeTestCase | LinkedListTestCase | GraphTestCase,
            Discriminator("type"),
        ]
    ]
    param_names: list[str]
