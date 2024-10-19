import pytest
from decimal import Decimal

from pydantic import ValidationError
from pytest import approx

from calculator.schemas import LoanInputSchema
from calculator.services import calculate_loan


def decimal_approx(value, abs=1e-6):
    return approx(value, abs=abs)


def test_basic_loan_calculation():
    input_data = LoanInputSchema(
        purchase_price=Decimal("200000"),
        down_payment=Decimal("40000"),
        down_payment_type="amount",
        mortgage_term=30,
        term_type="years",
        interest_rate=Decimal("4.5"),
    )
    result = calculate_loan(input_data)

    assert result.total_loan_amount == Decimal("160000.00")
    assert result.monthly_payment == decimal_approx(Decimal("810.70"))
    assert result.total_amount_paid == decimal_approx(Decimal("291850.74"))
    assert result.total_interest_paid == decimal_approx(Decimal("131850.74"))


def test_percentage_down_payment():
    input_data = LoanInputSchema(
        purchase_price=Decimal("300000"),
        down_payment=Decimal("20"),
        down_payment_type="percentage",
        mortgage_term=25,
        term_type="years",
        interest_rate=Decimal("3.75"),
    )
    result = calculate_loan(input_data)

    assert result.total_loan_amount == Decimal("240000.00")
    assert result.monthly_payment == decimal_approx(Decimal("1233.91"))
    assert result.total_amount_paid == decimal_approx(Decimal("370174.46"))
    assert result.total_interest_paid == decimal_approx(Decimal("130174.46"))


def test_mortgage_term_in_months():
    input_data = LoanInputSchema(
        purchase_price=Decimal("150000"),
        down_payment=Decimal("30000"),
        down_payment_type="amount",
        mortgage_term=240,
        term_type="months",
        interest_rate=Decimal("4"),
    )
    result = calculate_loan(input_data)

    assert result.total_loan_amount == Decimal("120000.00")
    assert result.monthly_payment == decimal_approx(Decimal("727.18"))
    assert result.total_amount_paid == decimal_approx(Decimal("174522.33"))
    assert result.total_interest_paid == decimal_approx(Decimal("54522.33"))


def test_zero_interest_rate():
    # Interest rate of 0% should raise a ValueError
    with pytest.raises(ValueError):
        LoanInputSchema(
            purchase_price=Decimal("100000"),
            down_payment=Decimal("20000"),
            down_payment_type="amount",
            mortgage_term=10,
            term_type="years",
            interest_rate=Decimal("0"),
        )


def test_full_down_payment():
    input_data = LoanInputSchema(
        purchase_price=Decimal("250000"),
        down_payment=Decimal("100"),
        down_payment_type="percentage",
        mortgage_term=15,
        term_type="years",
        interest_rate=Decimal("3.5"),
    )
    result = calculate_loan(input_data)

    assert result.total_loan_amount == Decimal("0.00")
    assert result.monthly_payment == Decimal("0.00")
    assert result.total_amount_paid == Decimal("0.00")
    assert result.total_interest_paid == Decimal("0.00")


def test_invalid_input():
    with pytest.raises(ValidationError):
        LoanInputSchema(
            purchase_price=Decimal("-100000"),
            down_payment=Decimal("20000"),
            down_payment_type="amount",
            mortgage_term=30,
            term_type="years",
            interest_rate=Decimal("4.5"),
        )

    with pytest.raises(ValidationError):
        LoanInputSchema(
            purchase_price=Decimal("100000"),
            down_payment=Decimal("20000"),
            down_payment_type="invalid",
            mortgage_term=30,
            term_type="years",
            interest_rate=Decimal("4.5"),
        )

    with pytest.raises(ValidationError):
        LoanInputSchema(
            purchase_price=Decimal("100000"),
            down_payment=Decimal("20000"),
            down_payment_type="amount",
            mortgage_term=30,
            term_type="decades",
            interest_rate=Decimal("4.5"),
        )

    with pytest.raises(ValidationError):
        LoanInputSchema(
            purchase_price=Decimal("100000"),
            down_payment=Decimal("20000"),
            down_payment_type="amount",
            mortgage_term=30,
            term_type="years",
            interest_rate=Decimal("350"),
        )
