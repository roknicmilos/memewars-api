import { API } from "./apiClient";
import { Meme } from "../models/Meme";
import { PageResponse } from "../models/PageResponse";

export const memeService = {

  async getMemes(warID: number, page: number = 1, pageSize: number = API.PAGE_SIZE): Promise<PageResponse> {
    const apiClient = API.createClient();
    const url = `/memes/?war=${ warID }&page=${ page }&ipp=${ pageSize }`;
    const response = await apiClient.get(url);
    return response.data;
  },

  async uploadMeme(warID: number, image: File): Promise<Meme> {
    const apiClient = API.createClient({ "Content-Type": "multipart/form-data" });
    const response = await apiClient.post("/memes/", { war: warID, image: image });
    return response.data;
  },

  async deleteMeme(memeID: number): Promise<void> {
    const apiClient = API.createClient();
    await apiClient.delete(`/memes/${ memeID }/`);
  },

};
