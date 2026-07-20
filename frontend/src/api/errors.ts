import axios, { type AxiosError } from "axios";

interface ApiErrorPayload {
  readonly error?: string;
  readonly message?: string;
  readonly details?: Record<string, unknown>;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: Record<string, unknown>;

  constructor(
    message: string,
    status: number,
    code: string,
    details: Record<string, unknown> = {},
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export function toApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiErrorPayload>;
    const status = axiosError.response?.status ?? 0;
    const payload = axiosError.response?.data;
    const message =
      payload?.message ?? axiosError.message ?? "Unexpected error";
    const code = payload?.error ?? "unknown_error";
    return new ApiError(message, status, code, payload?.details ?? {});
  }
  if (error instanceof Error) {
    return new ApiError(error.message, 0, "unknown_error");
  }
  return new ApiError("Unexpected error", 0, "unknown_error");
}