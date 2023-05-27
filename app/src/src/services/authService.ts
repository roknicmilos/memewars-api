import { API } from "./apiClient";

export const authService = {

  getLoginUrl(): string {
    const URLqueryParams = new URLSearchParams({
      login_success_redirect_url: `${ process.env.REACT_APP_APP_URL }/login-success/`,
      login_failure_redirect_url: `${ process.env.REACT_APP_APP_URL }/login-error/`,
    });
    return `${ process.env.REACT_APP_API_URL }/google-auth/login/?${ URLqueryParams.toString() }`;
  },

  async logout(): Promise<void> {
    const apiClient = API.createClient();
    await apiClient.get("/logout/");
  },

};
