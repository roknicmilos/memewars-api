import React, { useEffect, useState } from "react";
import { Meme } from "../../../../models/meme";
import { War } from "../../../../models/war";
import { memeService } from "../../../../services/memeService";
import styles from "./FinishedWar.module.scss";

interface FinishedWarProps {
  war: War;
}

export function FinishedWar({ war }: FinishedWarProps) {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ memes, setMemes ] = useState<Meme[]>([]);

  useEffect(() => {
    async function fetchMemes() {
      const memes = await memeService.getMemes(war.id);
      setMemes(memes);
      setIsLoading(false);
    }

    if (isLoading) {
      fetchMemes();
    }
  }, [ memes ]);

  return (
    <div className={ styles.memes }>
      { memes.map(meme => (
        <img className={ styles.meme } key={ meme.id } src={ meme.image } alt={ `meme ${ meme.id }` }/>)
      ) }
    </div>
  );
}
