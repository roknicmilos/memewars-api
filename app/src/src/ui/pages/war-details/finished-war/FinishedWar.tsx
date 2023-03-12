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
  const [ hasOpenedHeader, setHasOpenedHeader ] = useState<boolean>(false);


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

  function toggleHeader() {
    setHasOpenedHeader(!hasOpenedHeader);
  }

  const dropdownArrowClasses = [
    styles.dropdownArrow,
    hasOpenedHeader ? styles.dropdownArrowRotated : ""
  ].join(" ");

  const titleDropdownContentClasses = [
    styles.titleDropdownContent,
    hasOpenedHeader ? styles.titleDropdownContentOpened : ""
  ].join(" ");

  return (
    <>
      <div className={ styles.header }>
        <div className={ styles.titleDropdownButton } onClick={ toggleHeader }>
          <h1 className={ styles.title }>{ war.name }</h1>
          <img className={ dropdownArrowClasses } src={ dropdownVG } alt="carrot"/>
        </div>
        <div className={ titleDropdownContentClasses }>
          <div className={ styles.warInfo }>
            <p className={ styles.titleItem }>
              <span>Phase: </span>
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
      </div>
      <div className={ styles.memes }>
        { memes.sort(memeService.sortMemesByTotalScore).map(meme => (
          <FinishedWarMeme key={ meme.id } meme={ meme }/>
        )) }
      </div>
    </>
  );
}
