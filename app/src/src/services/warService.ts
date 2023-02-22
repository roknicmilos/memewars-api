import { War } from "../models/war";
import { apiClient } from "../apiClient";


export const warService = {

  async getWars(): Promise<War[]> {
    const response = await apiClient.get("/wars/");
    return response.data.items;
  }

};
