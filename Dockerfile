FROM python:3.10-slim

RUN mkdir /fastapi_dir
WORKDIR /fastapi_dir

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

COPY . .
WORKDIR src

CMD uvicorn main:app --workers 1 --host=0.0.0.0 --port=8080
