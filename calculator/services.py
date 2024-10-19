from calculator.schemas import LoanInputSchema, LoanOutputSchema


def calculate_loan(loan_input: LoanInputSchema) -> LoanOutputSchema:
    # Calculate the loan amount
    if loan_input.down_payment_type == "amount":
        loan_amount = loan_input.purchase_price - loan_input.down_payment
    else:  # percentage
        loan_amount = loan_input.purchase_price * (1 - loan_input.down_payment / 100)

    # Convert mortgage term to months if necessary
    if loan_input.term_type == "years":
        term_months = loan_input.mortgage_term * 12
    else:
        term_months = loan_input.mortgage_term

    # Calculate monthly interest rate
    monthly_interest_rate = loan_input.interest_rate / 12 / 100

    # Calculate monthly payment using the loan amortization formula
    monthly_payment = loan_amount * (
        (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months)
        / ((1 + monthly_interest_rate) ** term_months - 1)
    )

    # Calculate total amount paid and total interest paid
    total_amount_paid = monthly_payment * term_months
    total_interest_paid = total_amount_paid - loan_amount

    # Round results to two decimal places
    loan_amount = round(loan_amount, 2)
    monthly_payment = round(monthly_payment, 2)
    total_amount_paid = round(total_amount_paid, 2)
    total_interest_paid = round(total_interest_paid, 2)

    return LoanOutputSchema(
        total_loan_amount=loan_amount,
        monthly_payment=monthly_payment,
        total_amount_paid=total_amount_paid,
        total_interest_paid=total_interest_paid,
    )
