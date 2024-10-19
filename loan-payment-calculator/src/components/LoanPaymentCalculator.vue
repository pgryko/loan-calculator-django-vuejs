<template>
  <v-container>
    <h1 class="text-h4 mb-4">Loan Payment Calculator</h1>
    <v-row>
      <v-col cols="12" md="4">
        <v-form v-model="isFormValid" @submit.prevent="generateRates" ref="form">
          <v-text-field
            v-model="purchasePrice"
            label="Purchase Price*"
            prefix="$"
            type="number"
            placeholder="E.g. 100,000,000"
            :rules="[v => !!v || 'Purchase Price is required', v => v > 0 || 'Purchase Price must be greater than 0']"
            required
          ></v-text-field>
          <v-text-field
            v-model="interestRate"
            label="Interest Rate*"
            suffix="%"
            type="number"
            step="0.01"
            placeholder="E.g. 20%"
            :rules="[v => !!v || 'Interest Rate is required', v => v > 0 || 'Interest Rate must be greater than 0', v => v <= 100 || 'Interest Rate cannot exceed 100%']"
            required
          ></v-text-field>
          <v-text-field
            v-model="downPaymentDollars"
            label="Down Payment in $"
            prefix="$"
            type="number"
            placeholder="E.g. 15,000,000"
            :rules="[v => !v || v >= 0 || 'Down Payment cannot be negative', v => !v || v < purchasePrice || 'Down Payment cannot exceed Purchase Price']"
          ></v-text-field>
          <v-text-field
            v-model="downPaymentPercent"
            label="Down Payment in %"
            suffix="%"
            type="number"
            step="0.01"
            placeholder="E.g. 20%"
            :rules="[v => !v || (v >= 0 && v <= 100) || 'Down Payment % must be between 0 and 100']"
          ></v-text-field>
          <v-text-field
            v-model="mortgageTerm"
            label="Mortgage Term*"
            type="number"
            placeholder="E.g. 90 months"
            :rules="[v => !!v || 'Mortgage Term is required', v => v > 0 || 'Mortgage Term must be greater than 0', v => Number.isInteger(Number(v)) || 'Mortgage Term must be a whole number']"
            required
          ></v-text-field>
          <v-btn type="submit" color="primary" block :disabled="!isFormValid">Generate Rates</v-btn>
        </v-form>
      </v-col>
      <v-col cols="12" md="8">
        <v-table>
          <thead>
            <tr>
              <th>Mortgage Term</th>
              <th>Monthly Payment</th>
              <th>Interest Rate</th>
              <th>Total Amount</th>
              <th>Total over Loan Term</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in results" :key="index">
              <td>{{ result.term }} Years</td>
              <td>${{ result.monthlyPayment.toFixed(2) }}</td>
              <td>{{ result.interestRate.toFixed(2) }}%</td>
              <td>${{ result.totalAmount.toFixed(2) }}</td>
              <td>${{ result.totalOverTerm.toFixed(2) }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

interface LoanResult {
  term: number;
  monthlyPayment: number;
  interestRate: number;
  totalAmount: number;
  totalOverTerm: number;
}

export default defineComponent({
  name: 'LoanPaymentCalculator',
  setup() {
    const form = ref<any>(null);
    const isFormValid = ref(false);
    const purchasePrice = ref<number | null>(null);
    const interestRate = ref<number | null>(null);
    const downPaymentDollars = ref<number | null>(null);
    const downPaymentPercent = ref<number | null>(null);
    const mortgageTerm = ref<number | null>(null);
    const results = ref<LoanResult[]>([]);

    const calculateLoan = (term: number): LoanResult => {
      const principal = purchasePrice.value! - (downPaymentDollars.value || 0);
      const monthlyRate = (interestRate.value! / 100) / 12;
      const numberOfPayments = term * 12;

      const monthlyPayment =
        (principal * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
        (Math.pow(1 + monthlyRate, numberOfPayments) - 1);

      const totalAmount = monthlyPayment * numberOfPayments;
      return {
        term,
        monthlyPayment,
        interestRate: interestRate.value!,
        totalAmount,
        totalOverTerm: totalAmount - principal,
      };
    };

    const generateRates = () => {
      if (form.value.validate()) {
        const terms = [10, 15, 20, 25, 30];
        results.value = terms.map(term => calculateLoan(term));
      }
    };

    // Computed property to sync downPaymentDollars and downPaymentPercent
    const syncDownPayment = computed({
      get: () => downPaymentDollars.value,
      set: (value: number | null) => {
        if (value !== null && purchasePrice.value !== null) {
          downPaymentDollars.value = value;
          downPaymentPercent.value = (value / purchasePrice.value) * 100;
        }
      }
    });

    return {
      form,
      isFormValid,
      purchasePrice,
      interestRate,
      downPaymentDollars: syncDownPayment,
      downPaymentPercent,
      mortgageTerm,
      results,
      generateRates,
    };
  },
});
</script>
