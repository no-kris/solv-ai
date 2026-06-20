from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Discriminator


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


class ListNode(BaseModel):
    val: int
    next: Optional["ListNode"] = None


class TreeNode(BaseModel):
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


class GraphNode(BaseModel):
    val: int
    neighbors: list["GraphNode"] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GenericTestCase(BaseModel):
    type: Literal["generic"]
    params: dict[str, Any]
    expectedOutput: Any


class TreeTestCase(BaseModel):
    type: Literal["tree"]
    root: Optional[TreeNode] = None
    params: dict[str, Any] = {}
    expectedOutput: Optional[TreeNode] = None


class LinkedListTestCase(BaseModel):
    type: Literal["linked_list"]
    head: Optional[ListNode] = None
    params: dict[str, Any] = {}
    expectedOutput: Optional[ListNode] = None


class GraphTestCase(BaseModel):
    type: Literal["graph"]
    edges: dict[int, list[int]]
    start: Optional[GraphNode] = None
    target: Optional[GraphNode] = None
    params: dict[str, Any] = {}
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


# Update forward references
ListNode.model_rebuild()
TreeNode.model_rebuild()
GraphNode.model_rebuild()
