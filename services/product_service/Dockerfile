FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv
RUN uv sync --frozen
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
