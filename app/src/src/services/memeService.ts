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
    return currentMeme.total_score > nextMeme.total_score ? -1 : 0;
  },

  async uploadMeme(warID: number, image: File): Promise<Meme> {
    const apiClient = createAPIClient({ "Content-Type": "multipart/form-data" });
    const response = await apiClient.post("/memes/", { war: warID, image: image });
    return response.data;
  },

  async deleteMeme(memeID: number): Promise<void> {
    const apiClient = createAPIClient();
    await apiClient.delete(`/memes/${ memeID }`);
  },

};
