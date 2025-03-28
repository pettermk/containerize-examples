FROM registry.access.redhat.com/ubi9/ubi-minimal

RUN microdnf install python3
RUN mkdir /app
RUN chown 1000:0 /app
USER 1000
ENV HOME="/app"
COPY uv.lock pyproject.toml /app/
WORKDIR /app
RUN uv sync --frozen --no-install-project --no-editable --link-mode copy

COPY --chown=1000:1000 src/ /app/src
WORKDIR /app/src

CMD ["uv", "run", "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]

