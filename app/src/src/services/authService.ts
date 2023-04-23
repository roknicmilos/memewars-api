import { API } from "./apiClient";

export const authService = {

  getLoginUrl(): string {
    return `${ process.env.REACT_APP_API_URL }/google-auth/login/`;
  },

  async logout(): Promise<void> {
    const apiClient = API.createClient();
    await apiClient.get("/logout/");
  },

};
