import React, { useEffect, useState } from "react";
import { Meme } from "../../../../models/meme";
import { War } from "../../../../models/war";
import { memeService } from "../../../../services/memeService";
import styles from "./FinishedWar.module.scss";
import { FinishedWarMeme } from "./meme/FinishedWarMeme";
import dropdownVG from "../../../../assets/dropdown.svg";

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
    <>
      <div className={ styles.header }>
        <div className={ styles.titleDropdownButton }>
          <h1 className={ styles.title }>{ war.name }</h1>
          <img className={ styles.dropdownArrow } src={ dropdownVG } alt="carrot"/>
        </div>
        <div className={ styles.titleDropdownContent }>
          <p className={ styles.titleItem }>
            <span>War phase: </span>
            <span>{ war.phase }</span>
          </p>
          <p className={ styles.titleItem }>
            <span>Memes: </span>
            <span>{ war.meme_count }</span>
          </p>
          <p className={ styles.titleItem }>
            <span>Voters: </span>
            <span>{ war.voter_count }</span>
          </p>
          <p className={ styles.titleItem }>
            <span>Requires approval of memes? </span>
            <span>{ war.requires_meme_approval ? "YES" : "NO" }</span>
          </p>
        </div>
      </div>
      <div className={ styles.memes }>
        { memes.sort(memeService.sortMemesByTotalScore).map(meme => (
          <FinishedWarMeme key={ meme.id } meme={ meme }/>
        )) }
      </div>
    </>
  );
}
