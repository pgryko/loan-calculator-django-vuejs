/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LoanInputSchema } from '../models/LoanInputSchema'
import type { LoanOutputSchema } from '../models/LoanOutputSchema'
import type { CancelablePromise } from '../core/CancelablePromise'
import type { BaseHttpRequest } from '../core/BaseHttpRequest'
export class DefaultService {
  constructor(public readonly httpRequest: BaseHttpRequest) {}
  /**
   * Calculate Loan
   * @param requestBody
   * @returns LoanOutputSchema OK
   * @throws ApiError
   */
  public calculatorApiCalculateLoan(
    requestBody: LoanInputSchema,
  ): CancelablePromise<LoanOutputSchema> {
    return this.httpRequest.request({
      method: 'POST',
      url: '/api/calculator/calculate',
      body: requestBody,
      mediaType: 'application/json',
    })
  }
  /**
   * Save Scenario
   * @param requestBody
   * @returns any OK
   * @throws ApiError
   */
  public calculatorApiSaveScenario(
    requestBody: LoanInputSchema,
  ): CancelablePromise<any> {
    return this.httpRequest.request({
      method: 'POST',
      url: '/api/calculator/save-scenario',
      body: requestBody,
      mediaType: 'application/json',
    })
  }
  /**
   * Get Scenarios
   * @returns LoanOutputSchema OK
   * @throws ApiError
   */
  public calculatorApiGetScenarios(): CancelablePromise<
    Array<LoanOutputSchema>
  > {
    return this.httpRequest.request({
      method: 'GET',
      url: '/api/calculator/scenarios',
    })
  }
}
