import React from "react";
import { War } from "../../../../models/War";
import styles from "./FinishedWar.module.scss";
import { FinishedWarMeme } from "./meme/FinishedWarMeme";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";
import { useWarMemes } from "../../../../hooks/useWarMemes";

interface FinishedWarProps {
  war: War;
}

export function FinishedWar({ war }: FinishedWarProps) {
  const { memes, isLoading, memesBottomRef, nextPage } = useWarMemes(war.id);

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
