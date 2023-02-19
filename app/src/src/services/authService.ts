export const authService = {

  getLoginUrl(): string {
    return `${ process.env.REACT_APP_API_URL }/google-auth/login/`;
  }

};
