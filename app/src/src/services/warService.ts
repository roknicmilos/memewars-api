import { War } from "../models/War";
import { API } from "./apiClient";


export const warService = {

  async getWars(): Promise<War[]> {
    const apiClient = API.createClient();
    const response = await apiClient.get("/wars/");
    return response.data.results;
  },

  async getWar(warID: number): Promise<War> {
    const apiClient = API.createClient();
    const response = await apiClient.get(`/wars/${ warID }/`);
    return response.data;
  }

};
