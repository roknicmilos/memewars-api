import React from "react";
import styles from "./WarInSubmissionMeme.module.scss";
import { Meme } from "../../../../../models/meme";

interface WarInSubmissionMemeProps {
  meme: Meme;
}

export function WarInSubmissionMeme({ meme }: WarInSubmissionMemeProps) {

  return (
    <div className={ styles.meme }>
      <img className={ styles.memeImage } src={ meme.image } alt="meme"/>
    </div>
  );
}
