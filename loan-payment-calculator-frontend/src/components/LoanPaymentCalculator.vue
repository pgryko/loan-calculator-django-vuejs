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
        </v-form>
      </v-col>
      <v-col cols="12" md="8">
        <v-table v-if="loanOutputs.length > 0">
          <thead>
            <tr>
              <th
                v-for="header in headers"
                :key="header.value"
                @click="sort(header.value)"
              >
                {{ header.text }}
                <v-icon v-if="sortBy === header.value">
                  {{ sortDesc ? 'mdi-arrow-down' : 'mdi-arrow-up' }}
                </v-icon>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(output, index) in sortedLoanOutputs" :key="index">
              <td>${{ formatNumber(output.total_loan_amount) }}</td>
              <td>${{ formatNumber(output.monthly_payment) }}</td>
              <td>${{ formatNumber(output.total_amount_paid) }}</td>
              <td>${{ formatNumber(output.total_interest_paid) }}</td>
              <td>
                <v-btn icon small @click="deleteRow(index)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
        <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
      </v-col>
    </v-row>
    <v-dialog v-model="scenariosDialog" max-width="500px"> </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from 'vue'
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
    const scenariosDialog = ref(false)

    const loanOutputs = ref<LoanOutputSchema[]>([])
    const sortBy = ref<string>('total_loan_amount')
    const sortDesc = ref<boolean>(false)

    const headers = [
      { text: 'Total Loan Amount', value: 'total_loan_amount' },
      { text: 'Monthly Payment', value: 'monthly_payment' },
      { text: 'Total Amount Paid', value: 'total_amount_paid' },
      { text: 'Total Interest Paid', value: 'total_interest_paid' },
    ]

    const extractErrorMessage = (err: any): string => {
      if (err.body && err?.status === 422 && err?.body?.detail) {
        const detail = err.body.detail
        if (
          Array.isArray(detail) &&
          detail.length > 0 &&
          detail[0].ctx &&
          detail[0].ctx.error
        ) {
          return detail[0].ctx.error
        }
      }
      return 'An error occurred while calculating the loan. Please try again.'
    }

    const calculateLoan = async () => {
      try {
        error.value = null
        const result =
          await serverApi.default.calculatorApiCalculateLoan(loanInput)
        loanOutputs.value.push(result)
      } catch (err: any) {
        error.value = extractErrorMessage(err)
      }
    }

    const sort = (column: string) => {
      if (sortBy.value === column) {
        sortDesc.value = !sortDesc.value
      } else {
        sortBy.value = column
        sortDesc.value = false
      }
    }

    const sortedLoanOutputs = computed(() => {
      return [...loanOutputs.value].sort((a, b) => {
        const aValue = a[sortBy.value as keyof LoanOutputSchema]
        const bValue = b[sortBy.value as keyof LoanOutputSchema]
        if (aValue < bValue) return sortDesc.value ? 1 : -1
        if (aValue > bValue) return sortDesc.value ? -1 : 1
        return 0
      })
    })

    const deleteRow = (index: number) => {
      loanOutputs.value.splice(index, 1)
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
      scenariosDialog,
      calculateLoan,
      formatNumber,
      loanOutputs,
      sortedLoanOutputs,
      headers,
      sortBy,
      sortDesc,
      sort,
      deleteRow,
    }
  },
})
</script>
