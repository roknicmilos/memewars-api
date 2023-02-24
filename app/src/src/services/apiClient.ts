import axios, { AxiosInstance, CreateAxiosDefaults } from "axios";
import { authService } from "./authService";


export function createAPIClient(): AxiosInstance {
  const axiosConfig: CreateAxiosDefaults = {
    baseURL: process.env.REACT_APP_API_URL,
  };

  const user = authService.getUserFromLocalStorage();
  if (user) {
    axiosConfig.headers = { "Authorization": `Bearer ${ user.token }` };
  }

  return axios.create(axiosConfig);
}