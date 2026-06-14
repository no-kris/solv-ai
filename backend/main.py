from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas.schemas import CodingProblem, GenerateProblemRequest
from services.llm_service import generate_problem
from utils.config import get_allowed_origins
from utils.utils import structure_problem_data

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
    except Exception as e:
        print(f"Error: {e}")
        raise
