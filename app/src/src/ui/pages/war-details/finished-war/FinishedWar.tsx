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
  const { memes, isLoading } = useWarMemes(war.id);

  if (isLoading) return <Loader/>;

  return (
    <>
      <WarHeader war={ war }>
        <p>Memes are sorted by their score where those with the highest scores are at the top</p>
        <p>
          Check the voting results of <span className={ styles.boldText }>{ war.name }</span>.
        </p>
        { war.requires_meme_approval && (
          <p>
            Because this war requires approval of all memes,
            only the approved memes are listed below.
          </p>
        ) }
      </WarHeader>
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
