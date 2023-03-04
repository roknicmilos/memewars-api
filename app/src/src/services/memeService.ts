import { createAPIClient } from "./apiClient";
import { Meme } from "../models/meme";


export const memeService = {

  async getMemes(warID: number): Promise<Meme[]> {
    const apiClient = createAPIClient();
    const response = await apiClient.get(`/memes/?war=${ warID }`);
    return response.data.results;
  },

  sortMemesByTotalScore(currentMeme: Meme, nextMeme: Meme): number {
    if (currentMeme.total_score < nextMeme.total_score) {
      return 1;
    }
    if (currentMeme.total_score > nextMeme.total_score) {
      return -1;
    }
    return 0;
  },

};
