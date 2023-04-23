import React from "react";
import { Meme } from "../../../../../models/Meme";
import styles from "./FinishedWarMeme.module.scss";

interface FinishedWarMemeProps {
  meme: Meme;
}

export function FinishedWarMeme({ meme }: FinishedWarMemeProps) {
  return (
    <div className={ styles.meme }>
      <img
        className={ styles.memeImage }
        src={ meme.image }
        alt={ `meme ${ meme.id }` }
        onClick={ () => window.location.href = meme.image }/>
      <div className={ styles.memeScore }>{ meme.total_score }</div>
    </div>
  );
}
