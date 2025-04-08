FROM registry.access.redhat.com/ubi9/ubi-micro

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /app
RUN chown 1000:0 /app
USER 1000
ENV HOME="/app"
COPY requirements.txt /app/
WORKDIR /app
RUN uv python install
RUN uv venv
RUN uv pip install -r requirements.txt

COPY --chown=1000:0 src/ /app/src
WORKDIR /app/src

CMD ["uv", "run", "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]

