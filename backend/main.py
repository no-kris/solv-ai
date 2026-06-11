from fastapi import FastAPI

from schemas.schemas import CustomResponse
from services.llm_service import generate_problem

app = FastAPI(title="Solv.AI Backend API")


@app.get("/")
async def root():
    return {"status": "Solv.AI API up and running."}


@app.get("/test", response_model=CustomResponse)
async def testModel():
    return await generate_problem()
