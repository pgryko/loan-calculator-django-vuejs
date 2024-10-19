# Loan Payment Calculator

## Overview

The Loan Payment Calculator is a web application built with Django and Vue.js that allows users to calculate loan payments based on various input parameters. 
Users can try different scenarios to see how they affect their payments and view a history of their calculations.

## Features

- Calculate loan payments based on purchase price, down payment, mortgage term, and interest rate
- Support for down payment in both percentage and dollar amount
- Mortgage term input in years or months
- Display of total loan amount, monthly payment, total amount paid, and total interest paid
- Save and view multiple loan scenarios
- Responsive design for desktop and mobile devices

## Tech Stack

### Backend
- Django
- Django Ninja (for API)
- Sqlite (for development)
- Uvicorn (ASGI server)

### Frontend
- Vue.js

### DevOps
- Docker
- Docker Compose
- Poetry (for Python dependency management)

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js and yarn (for local frontend development)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/loan-payment-calculator.git
   cd loan-payment-calculator
   ```

2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:8000`

## Development

### Backend

1. Install Poetry:
   ```
   pip install poetry
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Activate the virtual environment:
   ```
   poetry shell
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```
   
6. Linting
   I use a combination of Ruff, Black, and Pylama for linting. To run the linters, use the following command:
    ```
    ruff check . --fix; black .; pylama
    ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   yarn install
   ```

3. Start the development server:
   ```
   yarn run serve
   ```

## Testing

Run the test suite using pytest:

```
pytest
```

## API Endpoints

- `POST /api/calculate`: Calculate loan payments
- `POST /api/save-scenario`: Save a loan scenario
- `GET /api/scenarios`: Retrieve all saved scenarios

For detailed API documentation, refer to the Django Ninja auto-generated API docs at `/api/docs`.

## Environment Variables

- `DEBUG`: Set to True for development, False for production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
