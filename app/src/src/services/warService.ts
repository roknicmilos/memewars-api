import { War } from "../models/war";
import { createAPIClient } from "./apiClient";


export const warService = {

  async getWars(): Promise<War[]> {
    const apiClient = createAPIClient();
    const response = await apiClient.get("/wars/");
    return response.data.results;
  }

};
