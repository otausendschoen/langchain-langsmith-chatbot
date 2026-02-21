# ---- Builder Stage ----
# 1. Use an official Python image as a parent image that has poetry pre-installed
FROM python:3.11-slim as builder

# 2. Set environment variables
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VENV="/opt/poetry/.venv"
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_VENV/bin:$POETRY_HOME/bin:$PATH"

# 3. Install poetry
RUN curl -sSL https://install.python-poetry.org | python -

# 4. Set the working directory in the container
WORKDIR /app

# 5. Copy the dependency files
COPY poetry.lock pyproject.toml ./

# 6. Install dependencies
RUN poetry install --no-dev --no-root

# ---- Final Stage ----
# 1. Use a slim Python image for the final image
FROM python:3.11-slim

# 2. Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory
WORKDIR /app

# 4. Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv .venv

# 5. Copy the rest of the application code
COPY src ./src
COPY docs ./docs

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Define the command to run your app
CMD ["uvicorn", "src.chatbot.api:app", "--host", "0.0.0.0", "--port", "8000"]
