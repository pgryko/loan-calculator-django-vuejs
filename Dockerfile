# Frontend build stage
FROM node:21 as frontend

WORKDIR /app

COPY loan-payment-calculator-frontend/package.json loan-payment-calculator-frontend/yarn.lock ./

RUN yarn install

COPY loan-payment-calculator-frontend .

RUN yarn build

# Backend build stage
FROM python:3.11 as backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

RUN poetry run python manage.py migrate
RUN poetry run python manage.py collectstatic --noinput

COPY --from=frontend /app/dist /app/static/frontend

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "loan_calculator.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
