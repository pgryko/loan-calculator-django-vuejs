from typing import List

from ninja import NinjaAPI


from .models import LoanScenario
from .schemas import LoanOutputSchema, LoanInputSchema
from .services import calculate_loan

api = NinjaAPI(
    urls_namespace="loan-calculator-api",
    version="0.1.0",
    title="Loan Calculator API",
)


@api.post("/calculate", response=LoanOutputSchema, url_name="calculate_loan")
def calculate_loan_api(request, loan_input: LoanInputSchema):

    return calculate_loan(loan_input)


@api.post("/save-scenario", url_name="save_scenario")
def save_scenario(request, loan_input: LoanInputSchema):
    calculation: LoanOutputSchema = calculate_loan(loan_input)
    scenario = LoanScenario.objects.create(
        purchase_price=loan_input.purchase_price,
        down_payment=loan_input.down_payment,
        down_payment_type=loan_input.down_payment_type,
        mortgage_term=loan_input.mortgage_term,
        term_type=loan_input.term_type,
        interest_rate=loan_input.interest_rate,
        total_loan_amount=calculation.total_loan_amount,
        monthly_payment=calculation.monthly_payment,
        total_amount_paid=calculation.total_amount_paid,
        total_interest_paid=calculation.total_interest_paid,
    )
    return {"id": scenario.id}


@api.get("/scenarios", response=List[LoanOutputSchema], url_name="get_scenarios")
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
