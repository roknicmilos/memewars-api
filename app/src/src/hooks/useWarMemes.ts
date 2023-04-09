import { Meme } from "../models/meme";
import { useEffect, useState } from "react";
import { memeService } from "../services/memeService";

export function useWarMemes(warID: number): [ Meme[], boolean ] {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ memes, setMemes ] = useState<Meme[]>([]);

  async function fetchMemes() {
    const memes = await memeService.getMemes(warID);
    setMemes(memes);
    setIsLoading(false);
  }

  useEffect(() => {
    if (isLoading) {
      fetchMemes();
    }
  }, []);

  return [ memes, isLoading ];
}
