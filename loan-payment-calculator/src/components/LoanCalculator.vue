<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-form @submit.prevent="generateRates">
          <v-text-field
            v-model="purchasePrice"
            label="Purchase Price *"
            placeholder="E.g. $100,000.000"
            prefix="$"
            required
          ></v-text-field>

          <v-text-field
            v-model="interestRate"
            label="Interest Rate *"
            placeholder="E.g. 20 %"
            suffix="%"
            required
          ></v-text-field>

          <v-text-field
            v-model="downPayment"
            label="Down Payment in $"
            placeholder="E.g. $15,000.000"
            prefix="$"
          ></v-text-field>

          <v-text-field
            v-model="downPaymentPercent"
            label="Down Payment in %"
            placeholder="E.g. 20 %"
            suffix="%"
          ></v-text-field>

          <v-text-field
            v-model="mortgageTerm"
            label="Mortgage Term *"
            placeholder="E.g. 90 months"
            required
          ></v-text-field>

          <v-btn color="primary" type="submit">Generate Rates</v-btn>
        </v-form>
      </v-col>

      <!-- Table Section -->
      <v-col cols="12" md="8">
        <v-data-table
          :headers="headers"
          :items="loanDetails"
          class="elevation-1"
        >
          <template v-slot:item.term="{ item }">
            <span>{{ item.term }} Years</span>
          </template>
          <template v-slot:item.payment="{ item }">
            <span>${{ item.payment }}</span>
          </template>
          <template v-slot:item.interestRate="{ item }">
            <span>{{ item.interestRate }}%</span>
          </template>
          <template v-slot:item.totalAmount="{ item }">
            <span>${{ item.totalAmount }}</span>
          </template>
          <template v-slot:item.totalOverTerm="{ item }">
            <span>${{ item.totalOverTerm }}</span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      purchasePrice: null,
      interestRate: null,
      downPayment: null,
      downPaymentPercent: null,
      mortgageTerm: null,
      loanDetails: [], // List of loan details to be displayed in the table
      headers: [
        { text: "Mortgage Term", value: "term" },
        { text: "Monthly Payment", value: "payment" },
        { text: "Interest Rate", value: "interestRate" },
        { text: "Total Amount", value: "totalAmount" },
        { text: "Total over Loan Term", value: "totalOverTerm" },
      ],
    };
  },
  methods: {
    generateRates() {
      // Function to generate the rates and populate loanDetails
      this.loanDetails = [
        {
          term: 15,
          payment: 2000,
          interestRate: 3.5,
          totalAmount: 300000,
          totalOverTerm: 360000,
        },
        {
          term: 30,
          payment: 1000,
          interestRate: 4.2,
          totalAmount: 350000,
          totalOverTerm: 420000,
        },
      ];
    },
  },
});
</script>

<style scoped>
.v-container {
  padding-top: 20px;
}

.v-data-table {
  margin-top: 20px;
}
</style>
