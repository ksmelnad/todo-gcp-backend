FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY main.py auth.py ./
COPY routes/ ./routes/
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
