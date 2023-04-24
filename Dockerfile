FROM python:3.10.9-slim

WORKDIR /usr/src/app

COPY pyproject.toml ./

RUN pip install --no-cache-dir --upgrade poetry && \
    poetry install --no-cache

EXPOSE 8000

CMD poetry run aerich upgrade && poetry run uvicorn server:app --reload --host 0.0.0.0 --root-path=/api/v1