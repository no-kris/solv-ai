import asyncio
import json

from pydantic import ValidationError

from prompts.build_prompt import build_prompt
from schemas.schemas import CodingProblem, CustomResponse
from utils.config import config


async def generate_problem(category: str, difficulty: str) -> CustomResponse:
    """
    Makes an API request to an LLM.
    Returns a CustomResponse object with fields:
        success
        error (optional)
        content (optional)
    Handles exceptions for:
        JSONDecodeError — LLM didn't return valid JSON
        ValidationError — JSON was valid but didn't match the `CodingProblem` schema
        TimeoutError — Request took too long
        Everything else as a fallback
    """
    try:
        prompt = build_prompt(category, difficulty)
        response = await config.get_client().chat_completion(
            messages=[{"role": "user", "content": prompt}], model=config.get_model()
        )
        content_str = str(response.choices[0].message.content)

        problem_data = json.loads(content_str)
        problem = CodingProblem(**problem_data)

        return CustomResponse(success=True, content=problem)
    except json.JSONDecodeError:
        return CustomResponse(success=False, error="LLM returned invalid JSON")
    except ValidationError:
        return CustomResponse(
            success=False, error="LLM returned invalid problem structure"
        )
    except asyncio.TimeoutError:
        return CustomResponse(success=False, error="Request timed out.")
    except Exception as e:
        print(f"DEBUG: {type(e).__name__}: {str(e)}")
        return CustomResponse(success=False, error="Failed to generate problem.")
