/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type LoanInputSchema = {
    purchase_price: (number | string);
    down_payment: (number | string);
    down_payment_type: LoanInputSchema.down_payment_type;
    mortgage_term: number;
    term_type: LoanInputSchema.term_type;
    interest_rate: (number | string);
};
export namespace LoanInputSchema {
    export enum down_payment_type {
        AMOUNT = 'amount',
        PERCENTAGE = 'percentage',
    }
    export enum term_type {
        YEARS = 'years',
        MONTHS = 'months',
    }
}

