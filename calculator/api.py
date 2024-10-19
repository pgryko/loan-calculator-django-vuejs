from typing import List, Literal

from ninja import NinjaAPI, Schema
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, field_validator

from .models import LoanScenario

api = NinjaAPI(
    urls_namespace="loan-calculator-api",
    version="0.1.0",
    title="Loan Calculator API",
)

# Whilst I've used the Decimal type, for production I would go with
# django-money which is based off py-moneyed and provides a dedicated MoneyField
class LoanInputSchema(BaseModel):
    purchase_price: Decimal = Field(gt=0)
    down_payment: Decimal = Field(ge=0)
    down_payment_type: Literal["amount", "percentage"]
    mortgage_term: int = Field(gt=0)
    term_type: Literal["years", "months"]
    interest_rate: Decimal = Field(gt=0, le=30)

    @model_validator(mode='after')
    def validate_down_payment(self) -> 'LoanInputSchema':
        if self.down_payment > self.purchase_price:
            raise ValueError('Down payment cannot be greater than purchase price')
        return self

    @field_validator('down_payment', 'purchase_price', 'interest_rate')
    @classmethod
    def round_decimal(cls, v: Decimal) -> Decimal:
        return v.quantize(Decimal('0.01'))

    model_config = {
        "json_encoders": {Decimal: str}
    }


class LoanOutputSchema(BaseModel):
    total_loan_amount: Decimal
    monthly_payment: Decimal
    total_amount_paid: Decimal
    total_interest_paid: Decimal


@api.post("/calculate", response=LoanOutputSchema)
def calculate_loan(request, loan_input: LoanInputSchema):
    # Implement loan calculation logic here
    # This is a placeholder implementation
    total_loan_amount = loan_input.purchase_price - (
        loan_input.down_payment
        if loan_input.down_payment_type == "amount"
        else loan_input.purchase_price * (loan_input.down_payment / 100)
    )

    term_months = (
        loan_input.mortgage_term * 12
        if loan_input.term_type == "years"
        else loan_input.mortgage_term
    )

    monthly_rate = loan_input.interest_rate / 12 / 100
    monthly_payment = (
        total_loan_amount * monthly_rate * (1 + monthly_rate) ** term_months
    ) / ((1 + monthly_rate) ** term_months - 1)

    total_amount_paid = monthly_payment * term_months
    total_interest_paid = total_amount_paid - total_loan_amount

    return {
        "total_loan_amount": total_loan_amount,
        "monthly_payment": monthly_payment,
        "total_amount_paid": total_amount_paid,
        "total_interest_paid": total_interest_paid,
    }


@api.post("/save-scenario")
def save_scenario(request, loan_input: LoanInputSchema):
    calculation = calculate_loan(request, loan_input)
    scenario = LoanScenario.objects.create(
        purchase_price=loan_input.purchase_price,
        down_payment=loan_input.down_payment,
        down_payment_type=loan_input.down_payment_type,
        mortgage_term=loan_input.mortgage_term,
        term_type=loan_input.term_type,
        interest_rate=loan_input.interest_rate,
        total_loan_amount=calculation["total_loan_amount"],
        monthly_payment=calculation["monthly_payment"],
        total_amount_paid=calculation["total_amount_paid"],
        total_interest_paid=calculation["total_interest_paid"],
    )
    return {"id": scenario.id}


@api.get("/scenarios", response=List[LoanOutputSchema])
def get_scenarios(request):
    scenarios = LoanScenario.objects.all().order_by("-created_at")
    return [
        {
            "total_loan_amount": scenario.total_loan_amount,
            "monthly_payment": scenario.monthly_payment,
            "total_amount_paid": scenario.total_amount_paid,
            "total_interest_paid": scenario.total_interest_paid,
        }
        for scenario in scenarios
    ]
