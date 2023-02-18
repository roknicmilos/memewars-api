import { User } from "../models/user";

export const authService = {

  mapURLQueryParamsToUser(params: URLSearchParams): User {
    this._validateUserURLQueryParams(params);
    return {
      token: params.get("token")!,
      email: params.get("email")!,
      firstName: params.get("first_name")!,
      lastName: params.get("last_name")!,
      imageURL: params.get("image_url") || "",
    };
  },

  _validateUserURLQueryParams(params: URLSearchParams): void {
    const requiredParamKeys = [ "token", "email", "first_name", "last_name" ];
    requiredParamKeys.forEach(paramKey => {
      if (!params.has(paramKey)) {
        throw Error(`Missing URL query parameter "${ paramKey }"`);
      }
    });
  },

  getLoginUrl(): string {
    return `${ process.env.REACT_APP_API_URL }/google-auth/login/`;
  }

};
