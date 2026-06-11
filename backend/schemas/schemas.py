from typing import Optional

from pydantic import BaseModel


class CustomResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    content: Optional[str] = None
