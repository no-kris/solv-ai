import asyncio

from huggingface_hub import AsyncInferenceClient

from schemas.schemas import CustomResponse
from utils.config import config


async def generate_problem() -> CustomResponse:
    try:
        client = AsyncInferenceClient(token=config.get_hf_token())
        response = await client.chat_completion(
            messages=[{"role": "user", "content": "hello"}], model=config.get_model()
        )
        content = response.choices[0].message.content

        if not content:
            return CustomResponse(success=False, error="Empty response from model")

        return CustomResponse(success=True, content=content)
    except asyncio.TimeoutError:
        return CustomResponse(success=False, error="Request timed out.")
    except Exception as e:
        print(f"DEBUG: {type(e).__name__}: {str(e)}")
        return CustomResponse(success=False, error="Faield to generate problem.")
