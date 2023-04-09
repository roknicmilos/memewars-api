import React, { useState } from "react";
import { War } from "../../../../models/war";
import { memeService } from "../../../../services/memeService";
import styles from "./FinishedWar.module.scss";
import { FinishedWarMeme } from "./meme/FinishedWarMeme";
import { useWarMemes } from "../../../../hooks/useWarMemes";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";

interface FinishedWarProps {
  war: War;
}

export function FinishedWar({ war }: FinishedWarProps) {
  const [ memes, isLoading ] = useWarMemes(war.id);
  const [ hasOpenedHeader, setHasOpenedHeader ] = useState<boolean>(false);

  function toggleHeader() {
    setHasOpenedHeader(!hasOpenedHeader);
  }

  if (isLoading) return <Loader/>;

  return (
    <>
      <WarHeader
        war={ war }
        isOpened={ hasOpenedHeader }
        onClick={ toggleHeader }
        extraInfoItems={ [ { label: "Voters", value: war.voter_count } ] }
      />
      <div className={ styles.memes }>
        { memes.sort(memeService.sortMemesByTotalScore).map(meme => (
          <FinishedWarMeme key={ meme.id } meme={ meme }/>
        )) }
      </div>
      <div className={ styles.rockBottom }>
        <p>You've finally hit rock bottom!</p>
        <p>At least you can't get lower that this 🥲</p>
      </div>
    </>
  );
}
