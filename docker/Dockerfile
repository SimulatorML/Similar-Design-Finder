FROM python:3.11.9-slim-bookworm as poetry-dependencies

WORKDIR /tmp
RUN apt-get -y update && apt-get -y upgrade && pip install poetry && rm -rf /var/lib/apt/lists/*
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

# ---------------------------------------------------------------

FROM python:3.11.9-slim-bookworm

WORKDIR /app

COPY --from=poetry-dependencies /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY .env.local* .env.test* .env.prod* /app/

EXPOSE 8080
CMD ["uvicorn", "src.app.app:app", "--host", "0.0.0.0", "--port", "8080"]
