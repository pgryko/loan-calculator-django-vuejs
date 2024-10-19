<template>
  <v-container>
    <h1 class="text-h4 mb-4">Loan Payment Calculator</h1>
    <v-row>
      <v-col cols="12" md="4">
        <v-form
          v-model="isFormValid"
          @submit.prevent="calculateLoan"
          ref="form"
        >
          <v-text-field
            v-model="loanInput.purchase_price"
            label="Purchase Price*"
            prefix="$"
            type="number"
            placeholder="E.g. 100000000"
            :rules="[
              v => !!v || 'Purchase Price is required',
              v => v > 0 || 'Purchase Price must be greater than 0',
            ]"
            required
          ></v-text-field>
          <v-text-field
            v-model="loanInput.interest_rate"
            label="Interest Rate*"
            suffix="%"
            type="number"
            step="0.01"
            placeholder="E.g. 20"
            :rules="[
              v => !!v || 'Interest Rate is required',
              v => v > 0 || 'Interest Rate must be greater than 0',
              v => v <= 100 || 'Interest Rate cannot exceed 100%',
            ]"
            required
          ></v-text-field>
          <v-text-field
            v-model="loanInput.down_payment"
            :label="`Down Payment in ${loanInput.down_payment_type === 'amount' ? '$' : '%'}*`"
            :prefix="loanInput.down_payment_type === 'amount' ? '$' : ''"
            :suffix="loanInput.down_payment_type === 'percentage' ? '%' : ''"
            type="number"
            step="0.01"
            placeholder="E.g. 15000000 or 20"
            :rules="[
              v => !!v || 'Down Payment is required',
              v => v >= 0 || 'Down Payment cannot be negative',
            ]"
            required
          ></v-text-field>
          <v-radio-group v-model="loanInput.down_payment_type" row>
            <v-radio label="Amount" value="amount"></v-radio>
            <v-radio label="Percentage" value="percentage"></v-radio>
          </v-radio-group>
          <v-text-field
            v-model="loanInput.mortgage_term"
            label="Mortgage Term*"
            type="number"
            placeholder="E.g. 90"
            :rules="[
              v => !!v || 'Mortgage Term is required',
              v => v > 0 || 'Mortgage Term must be greater than 0',
              v =>
                Number.isInteger(Number(v)) ||
                'Mortgage Term must be a whole number',
            ]"
            required
          ></v-text-field>
          <v-radio-group v-model="loanInput.term_type" row>
            <v-radio label="Months" value="months"></v-radio>
            <v-radio label="Years" value="years"></v-radio>
          </v-radio-group>
          <v-btn
            type="submit"
            color="primary"
            block
            :disabled="!isFormValid"
            class="mt-4"
            >Calculate Loan</v-btn
          >
          <v-btn color="secondary" block @click="saveScenario" class="mt-2"
            >Save Scenario</v-btn
          >
          <v-btn color="info" block @click="loadScenarios" class="mt-2"
            >Load Scenarios</v-btn
          >
        </v-form>
      </v-col>
      <v-col cols="12" md="8">
        <v-table v-if="loanOutput">
          <thead>
            <tr>
              <th>Total Loan Amount</th>
              <th>Monthly Payment</th>
              <th>Total Amount Paid</th>
              <th>Total Interest Paid</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>${{ formatNumber(loanOutput.total_loan_amount) }}</td>
              <td>${{ formatNumber(loanOutput.monthly_payment) }}</td>
              <td>${{ formatNumber(loanOutput.total_amount_paid) }}</td>
              <td>${{ formatNumber(loanOutput.total_interest_paid) }}</td>
            </tr>
          </tbody>
        </v-table>
        <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
      </v-col>
    </v-row>
    <v-dialog v-model="scenariosDialog" max-width="500px">
      <v-card>
        <v-card-title>Saved Scenarios</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item
              v-for="(scenario, index) in savedScenarios"
              :key="index"
              @click="loadScenario(scenario)"
            >
              <v-list-item-title>Scenario {{ index + 1 }}</v-list-item-title>
              <v-list-item-subtitle
                >${{ formatNumber(scenario.total_loan_amount) }} / ${{
                  formatNumber(scenario.monthly_payment)
                }}
                per month</v-list-item-subtitle
              >
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="scenariosDialog = false"
            >Close</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue'
import { LoanInputSchema, LoanOutputSchema } from '@/gen/server'
import { serverApi } from '@/apis/serverApi'

export default defineComponent({
  name: 'LoanPaymentCalculator',
  setup() {
    const form = ref<any>(null)
    const isFormValid = ref(false)
    const loanInput = reactive<LoanInputSchema>({
      purchase_price: '',
      down_payment: '',
      down_payment_type: LoanInputSchema.down_payment_type.AMOUNT,
      mortgage_term: 0,
      term_type: LoanInputSchema.term_type.YEARS,
      interest_rate: '',
    })
    const loanOutput = ref<LoanOutputSchema | null>(null)
    const error = ref<string | null>(null)
    const savedScenarios = ref<LoanOutputSchema[]>([])
    const scenariosDialog = ref(false)

    const calculateLoan = async () => {
      try {
        error.value = null
        loanOutput.value = await serverApi.calculatorApiCalculateLoan(loanInput)
      } catch (err) {
        error.value =
          'An error occurred while calculating the loan. Please try again.'
        console.error(err)
      }
    }

    const saveScenario = async () => {
      try {
        await serverApi.calculatorApiSaveScenario(loanInput)
        alert('Scenario saved successfully!')
      } catch (err) {
        alert('Failed to save scenario. Please try again.')
        console.error(err)
      }
    }

    const loadScenarios = async () => {
      try {
        savedScenarios.value = await serverApi.calculatorApiGetScenarios()
        scenariosDialog.value = true
      } catch (err) {
        alert('Failed to load scenarios. Please try again.')
        console.error(err)
      }
    }

    const loadScenario = (scenario: LoanOutputSchema) => {
      loanOutput.value = scenario
      scenariosDialog.value = false
    }

    const formatNumber = (value: number | string): string => {
      return Number(value).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })
    }

    return {
      form,
      isFormValid,
      loanInput,
      loanOutput,
      error,
      savedScenarios,
      scenariosDialog,
      calculateLoan,
      saveScenario,
      loadScenarios,
      loadScenario,
      formatNumber,
    }
  },
})
</script>
