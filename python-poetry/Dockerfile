FROM registry.access.redhat.com/ubi9/ubi-micro

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /app
RUN chown 1000:0 /app
USER 1000
ENV HOME="/app"
ENV DATABASE_URL="postgresql+psycopg://postgres:12345@host.docker.internal:5432/todos"
COPY poetry.lock pyproject.toml /app/
WORKDIR /app
RUN uv python install
RUN uv tool install poetry
RUN uvx poetry install --no-root

COPY --chown=1000:0 src/ /app/src

CMD ["uvx", "poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]

