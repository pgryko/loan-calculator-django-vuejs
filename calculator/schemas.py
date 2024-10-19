from typing import Literal

from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, field_validator


# Whilst I've used the Decimal type, for production I would go with
# django-money which is based off py-moneyed and provides a dedicated MoneyField
class LoanInputSchema(BaseModel):
    purchase_price: Decimal = Field(gt=0)
    down_payment: Decimal = Field(ge=0)
    down_payment_type: Literal["amount", "percentage"]
    mortgage_term: int = Field(gt=0)
    term_type: Literal["years", "months"]
    interest_rate: Decimal = Field(gt=0, le=100)

    @model_validator(mode="after")
    def validate_down_payment(self) -> "LoanInputSchema":
        if self.down_payment > self.purchase_price:
            raise ValueError("Down payment cannot be greater than purchase price")
        return self

    @classmethod
    @field_validator("down_payment", "purchase_price", "interest_rate")
    def round_decimal(cls, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.01"))

    model_config = {"json_encoders": {Decimal: str}}


class LoanOutputSchema(BaseModel):
    total_loan_amount: Decimal
    monthly_payment: Decimal
    total_amount_paid: Decimal
    total_interest_paid: Decimal
