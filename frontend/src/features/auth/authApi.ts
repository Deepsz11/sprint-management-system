import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type { AuthUser, LoginCredentials, TokenPair } from "./types";

export const authApi = {
  async login(credentials: LoginCredentials): Promise<TokenPair> {
    const params = new URLSearchParams();
    params.append("username", credentials.email);
    params.append("password", credentials.password);

    const response = await apiClient.post<TokenPair>(
      API_ENDPOINTS.AUTH.LOGIN,
      params,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      },
    );
    return response.data;
  },

  async me(): Promise<AuthUser> {
    const response = await apiClient.get<AuthUser>(API_ENDPOINTS.AUTH.ME);
    return response.data;
  },

  async logout(refreshToken: string): Promise<void> {
    await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT, {
      refresh_token: refreshToken,
    });
  },
};