# calculator/tests/test_api.py

import pytest
from django.urls import reverse

from calculator.api import LoanInputSchema
from calculator.models import LoanScenario
from decimal import Decimal
from django.test.client import Client

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return Client()


def test_calculate_loan(api_client):
    url = reverse("loan-calculator-api:calculate_loan")
    data = LoanInputSchema(
        **{
            "purchase_price": "300000.00",
            "down_payment": "60000.00",
            "down_payment_type": "amount",
            "mortgage_term": 30,
            "term_type": "years",
            "interest_rate": "3.5",
        }
    )
    response = api_client.post(
        url, data.model_dump_json(), content_type="application/json"
    )
    assert response.status_code == 200
    result = response.json()

    assert "total_loan_amount" in result
    assert "monthly_payment" in result
    assert "total_amount_paid" in result
    assert "total_interest_paid" in result

    assert Decimal(result["total_loan_amount"]) == Decimal("240000.00")
    assert round(Decimal(result["monthly_payment"]), 2) == Decimal("1077.71")


def test_calculate_loan_percentage_down_payment(api_client):
    url = reverse("loan-calculator-api:calculate_loan")
    data = {
        "purchase_price": "300000.00",
        "down_payment": "20",
        "down_payment_type": "percentage",
        "mortgage_term": 360,
        "term_type": "months",
        "interest_rate": "3.5",
    }
    response = api_client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    result = response.json()

    assert Decimal(result["total_loan_amount"]) == Decimal("240000.00")


def test_save_scenario(api_client):
    url = reverse("loan-calculator-api:save_scenario")
    data = {
        "purchase_price": "300000.00",
        "down_payment": "60000.00",
        "down_payment_type": "amount",
        "mortgage_term": 30,
        "term_type": "years",
        "interest_rate": "3.5",
    }
    response = api_client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    result = response.json()

    assert "id" in result
    scenario_id = result["id"]

    saved_scenario = LoanScenario.objects.get(id=scenario_id)
    assert saved_scenario.purchase_price == Decimal("300000.00")
    assert saved_scenario.down_payment == Decimal("60000.00")
    assert saved_scenario.mortgage_term == 30
    assert saved_scenario.interest_rate == Decimal("3.5")


def test_get_scenarios(api_client):
    # Create some test scenarios
    LoanScenario.objects.create(
        purchase_price=Decimal("300000.00"),
        down_payment=Decimal("60000.00"),
        down_payment_type="amount",
        mortgage_term=30,
        term_type="years",
        interest_rate=Decimal("3.5"),
        total_loan_amount=Decimal("240000.00"),
        monthly_payment=Decimal("1077.71"),
        total_amount_paid=Decimal("387975.60"),
        total_interest_paid=Decimal("147975.60"),
    )

    url = reverse("loan-calculator-api:get_scenarios")
    response = api_client.get(url)
    assert response.status_code == 200
    result = response.json()

    assert len(result) > 0
    scenario = result[0]
    assert "total_loan_amount" in scenario
    assert "monthly_payment" in scenario
    assert "total_amount_paid" in scenario
    assert "total_interest_paid" in scenario


@pytest.mark.parametrize(
    "purchase_price,down_payment,down_payment_type,mortgage_term,term_type,interest_rate,expected_status",
    [
        ("300000.00", "60000.00", "amount", 30, "years", "3.5", 200),
        ("0", "0", "amount", 30, "years", "3.5", 422),
        ("300000.00", "-1000", "amount", 30, "years", "3.5", 422),
        ("300000.00", "60000.00", "invalid", 30, "years", "3.5", 422),
        ("300000.00", "60000.00", "amount", 0, "years", "3.5", 422),
        ("300000.00", "60000.00", "amount", 30, "invalid", "3.5", 422),
        ("300000.00", "60000.00", "amount", 30, "years", "-1", 422),
    ],
)
def test_input_validation(
    api_client,
    purchase_price,
    down_payment,
    down_payment_type,
    mortgage_term,
    term_type,
    interest_rate,
    expected_status,
):
    url = reverse("loan-calculator-api:calculate_loan")
    data = {
        "purchase_price": purchase_price,
        "down_payment": down_payment,
        "down_payment_type": down_payment_type,
        "mortgage_term": mortgage_term,
        "term_type": term_type,
        "interest_rate": interest_rate,
    }
    response = api_client.post(url, data, content_type="application/json")
    assert response.status_code == expected_status
