import { createAPIClient } from "./apiClient";
import { Meme } from "../models/meme";


export const memeService = {

  async getMemes(warID: number): Promise<Meme[]> {
    const apiClient = createAPIClient();
    const response = await apiClient.get(`/memes/?war=${ warID }`);
    return response.data.results;
  }

};
