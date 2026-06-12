import asyncio
import json
import random

from pydantic import ValidationError

from prompts.build_prompt import build_prompt, get_node_structure
from schemas.schemas import CodingProblem, CustomResponse
from utils.config import config


async def generate_problem(
    category: str, difficulty: str, max_retries: int = 3
) -> CustomResponse:
    """
    Makes an API request to an LLM with retry logic.
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
    for attempt in range(max_retries):
        if attempt > 0:
            delay = (2**attempt) + random.uniform(0, 0.5)
            await asyncio.sleep(delay)
        try:
            prompt = build_prompt(category, difficulty)
            response = await config.get_client().chat_completion(
                messages=[{"role": "user", "content": prompt}], model=config.get_model()
            )
            content_str = str(response.choices[0].message.content)

            problem_data = json.loads(content_str)
            problem = CodingProblem(**problem_data)
            problem.nodeStructure = get_node_structure(category)

            return CustomResponse(success=True, content=problem)

        except json.JSONDecodeError:
            if attempt == max_retries - 1:
                return CustomResponse(
                    success=False,
                    error=f"LLM returned invalid JSON after {max_retries} retries",
                )
            print(f"Attempt {attempt + 1}: JSON parse error, retrying...")
            continue

        except ValidationError:
            if attempt == max_retries - 1:
                return CustomResponse(
                    success=False,
                    error=f"LLM returned invalid schema after {max_retries} retries",
                )
            print(f"Attempt {attempt + 1}: Schema validation failed, retrying...")
            continue

        except asyncio.TimeoutError:
            return CustomResponse(success=False, error="Request timed out.")

        except Exception as e:
            if attempt == max_retries - 1:
                return CustomResponse(
                    success=False, error="Failed to generate problem."
                )
            print(f"Attempt {attempt + 1}: {type(e).__name__}, retrying...")
            continue

    return CustomResponse(
        success=False, error="Failed to generate problem after all retries"
    )
