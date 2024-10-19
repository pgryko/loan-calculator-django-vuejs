<!--<template>-->
<!--  <v-app>-->
<!--    <v-main>-->
<!--      <loan-calculator />-->
<!--    </v-main>-->
<!--  </v-app>-->
<!--</template>-->

<!--<script lang="ts">-->
<!--import LoanCalculator from "./components/LoanCalculator.vue";-->

<!--export default {-->
<!--  components: {-->
<!--    LoanCalculator,-->
<!--  },-->
<!--};-->
<!--</script>-->

<template>
  <v-app>
    <v-main>
      <LoanPaymentCalculator />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LoanPaymentCalculator from './components/LoanPaymentCalculator.vue';

export default defineComponent({
  name: 'App',
  components: {
    LoanPaymentCalculator,
  },
});
</script>
