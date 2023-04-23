import React, { useEffect, useRef, useState } from "react";
import { War } from "../../../../models/War";
import { memeService } from "../../../../services/memeService";
import styles from "./FinishedWar.module.scss";
import { FinishedWarMeme } from "./meme/FinishedWarMeme";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";
import { Meme } from "../../../../models/Meme";
import { useVisible } from "../../../../hooks/useVisible";
import { API } from "../../../../services/apiClient";

interface FinishedWarProps {
  war: War;
}

export function FinishedWar({ war }: FinishedWarProps) {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ memes, setMemes ] = useState<Meme[]>([]);
  const [ nextPage, setNextPage ] = useState<number | undefined>(1);
  const memesBottomRef = useRef(null);
  const isSeeingEndOfList = useVisible(memesBottomRef);

  async function fetchMemes() {
    if (nextPage === undefined) {
      throw Error("Unable to fetch the next page of memes because there is no next page");
    }
    const pageResponse = await memeService.getMemes(war.id, nextPage);
    setMemes([ ...memes, ...pageResponse.results ]);
    const hasNextPage = pageResponse.count / API.PAGE_SIZE > nextPage;
    setNextPage(hasNextPage ? nextPage + 1 : undefined);
    setIsLoading(false);
  }

  useEffect(() => {
    if (isLoading || (isSeeingEndOfList && nextPage)) {
      fetchMemes();
    }
  }, [ isSeeingEndOfList ]);

  if (isLoading) return <Loader/>;

  return (
    <>
      <WarHeader war={ war }>
        <p>These are the voting results of <span className={ styles.boldText }>{ war.name }</span>.</p>
        <p>Memes are sorted by their score where those with the highest score are at the top.</p>
        { war.requires_meme_approval && (
          <p>
            Because this war requires approval of all memes,
            only the approved memes are listed below.
          </p>
        ) }
      </WarHeader>
      <div className={ styles.memes }>
        { memes.map(meme => <FinishedWarMeme key={ meme.id } meme={ meme }/>) }
      </div>
      <div ref={ memesBottomRef }></div>
      { !nextPage && (
        <div className={ styles.rockBottom }>
          <p>You've finally hit rock bottom!</p>
          <p>At least you can't get lower that this 🥲</p>
        </div>
      ) }
    </>
  );
}
