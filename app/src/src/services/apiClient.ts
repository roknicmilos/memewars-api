import axios, { AxiosInstance, CreateAxiosDefaults } from "axios";
import { localStorageService } from "./localStorageService";


export function createAPIClient(): AxiosInstance {
  const axiosConfig: CreateAxiosDefaults = {
    baseURL: process.env.REACT_APP_API_URL,
  };

  const user = localStorageService.getUser();
  if (user) {
    axiosConfig.headers = { "Authorization": `Bearer ${ user.token }` };
  }

  return axios.create(axiosConfig);
}
