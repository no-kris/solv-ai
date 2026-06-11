from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.schemas import CustomResponse, GenerateProblemRequest
from services.llm_service import generate_problem
from utils.config import get_allowed_origins

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


@app.post("/api/generate-problem", response_model=CustomResponse)
async def api_generate_problem(
    request: GenerateProblemRequest,
):
    return await generate_problem(
        category=request.category, difficulty=request.difficulty
    )
