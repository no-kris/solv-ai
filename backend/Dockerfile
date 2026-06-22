FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY backend/ .

RUN uv sync

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
