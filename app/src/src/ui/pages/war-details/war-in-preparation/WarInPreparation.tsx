import React from "react";
import { War } from "../../../../models/War";
import styles from "./../../../main.module.scss";
import { WarHeader } from "../../../components/war-header/WarHeader";

interface WarInPreparationProps {
  war: War;
}

export function WarInPreparation({ war }: WarInPreparationProps) {
  return (
    <WarHeader war={ war }>
      <p><span className={ styles.boldText }>{ war.name }</span> is still being prepared ‍🛠️</p>
      <p>After we finish preparing this war, you will be able to upload your memes to it.</p>
      { war.requires_meme_approval && (
        <p>Each meme that you upload to the war has to be approved so others could see and rate it.</p>
      ) }
    </WarHeader>
  );
}
