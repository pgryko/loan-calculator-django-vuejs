from django.db import models


class LoanScenario(models.Model):
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment_type = models.CharField(
        max_length=10, choices=[("percent", "Percent"), ("amount", "Amount")]
    )
    mortgage_term = models.IntegerField()
    term_type = models.CharField(
        max_length=10, choices=[("years", "Years"), ("months", "Months")]
    )
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    total_interest_paid = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Scenario {self.id} - ${self.purchase_price}"
