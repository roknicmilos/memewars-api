import { Meme } from "../models/Meme";
import { MutableRefObject, useEffect, useRef, useState } from "react";
import { memeService } from "../services/memeService";
import { useVisible } from "./useVisible";
import { API } from "../services/apiClient";

interface UseWarMemesReturnValue {
  memes: Meme[];
  setMemes(memes: Meme[]): void;
  isLoading: boolean;
  setIsLoading(isLoading: boolean): void;
  memesBottomRef: MutableRefObject<null>;
  nextPage?: number;
}

export function useWarMemes(warID: number, pageSize: number = API.PAGE_SIZE): UseWarMemesReturnValue {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ memes, setMemes ] = useState<Meme[]>([]);
  const [ nextPage, setNextPage ] = useState<number | undefined>(1);
  const memesBottomRef = useRef(null);
  const isSeeingEndOfList = useVisible(memesBottomRef);

  async function fetchMemes() {
    if (nextPage === undefined) {
      throw Error("Unable to fetch the next page of memes because there is no next page");
    }
    const pageResponse = await memeService.getMemes(warID, nextPage, pageSize);
    setMemes([ ...memes, ...pageResponse.results ]);
    const hasNextPage = pageResponse.count / pageSize > nextPage;
    setNextPage(hasNextPage ? nextPage + 1 : undefined);
    setIsLoading(false);
  }

  useEffect(() => {
    if (isLoading || (isSeeingEndOfList && nextPage)) {
      fetchMemes();
    }
  }, [ isSeeingEndOfList ]);

  return { memes, setMemes, isLoading, setIsLoading, memesBottomRef, nextPage };
}
