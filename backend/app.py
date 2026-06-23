import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas.schemas import (
    CodingProblem,
    CustomResponse,
    GenerateProblemRequest,
    ValidateProblemRequest,
    ValidationResponse,
)
from services.llm_service import generate_problem
from utils.config import get_allowed_origins
from utils.execute import execute_code
from utils.utils import structure_problem_data
from utils.validation import has_dangerous_imports, validate_parameters

app = FastAPI(title="Solv.AI Backend API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    expose_headers=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "Solv.AI API up and running."}


@app.post("/api/validate-problem")
async def api_validate_problem(
    request: ValidateProblemRequest, response_model=ValidationResponse
):
    # print(f"Problem: {request.tests}")
    try:
        is_valid = validate_parameters(request.code, request.param_names)
        if not is_valid.success:
            raise HTTPException(status_code=400, detail=is_valid.error)

        is_dangerous = has_dangerous_imports(request.code)
        if is_dangerous.success:
            raise HTTPException(status_code=400, detail=is_dangerous.error)

        result = execute_code(request.code, request.tests, request.param_names)

        if isinstance(result, CustomResponse) and not result.success:
            raise HTTPException(status_code=400, detail=result.error)

        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/generate-problem", response_model=CodingProblem)
async def api_generate_problem(
    request: GenerateProblemRequest,
):
    try:
        problem_data = await generate_problem(
            category=request.category, difficulty=request.difficulty
        )

        if not problem_data.success:
            raise HTTPException(status_code=400, detail=problem_data.error)

        structured_problem_data = structure_problem_data(
            problem_data.content, request.category
        )

        if not structured_problem_data:
            raise HTTPException(
                status_code=400,
                detail="Problem data does not match the schema.",
            )

        return structured_problem_data
    except Exception:
        print(f"Error: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail="An unexpected error occurred.")
