import { API } from "./apiClient";
import { Meme } from "../models/Meme";
import { PageResponse } from "../models/PageResponse";

export const memeService = {

  async getMemes(warID: number, page: number = 1): Promise<PageResponse> {
    const apiClient = API.createClient();
    const response = await apiClient.get(`/memes/?war=${ warID }&page=${ page }`);
    return response.data;
  },

  async uploadMeme(warID: number, image: File): Promise<Meme> {
    const apiClient = API.createClient({ "Content-Type": "multipart/form-data" });
    const response = await apiClient.post("/memes/", { war: warID, image: image });
    return response.data;
  },

  async deleteMeme(memeID: number): Promise<void> {
    const apiClient = API.createClient();
    await apiClient.delete(`/memes/${ memeID }`);
  },

};
