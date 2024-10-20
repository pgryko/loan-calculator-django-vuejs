import { Server } from '@/gen/server'

const getBaseUrl = (): string => {
  // if (process.env.NODE_ENV === "development") {
  return process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'
  // }
  // For production or any other environment
  // return process.env.VUE_APP_API_BASE_URL || "";
}

export const serverApi = new Server({
  BASE: getBaseUrl(),
  // Add other configuration options here if needed
})
