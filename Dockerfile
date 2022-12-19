FROM python:3.10.9-bullseye

WORKDIR /usr/src/app

COPY pyproject.toml ./

RUN pip install poetry && \
    poetry install

EXPOSE 8000

CMD poetry run uvicorn server:app --reload --host 0.0.0.0