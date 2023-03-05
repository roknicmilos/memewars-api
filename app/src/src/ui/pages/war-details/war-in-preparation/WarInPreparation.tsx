import React from "react";
import { War } from "../../../../models/war";
import styles from "./WarInPreparation.module.scss";

interface WarInPreparationProps {
  war: War;
}

export function WarInPreparation({ war }: WarInPreparationProps) {
  return (
    <div className={ styles.container }>
      <p className={ styles.text }>
        <span className={ styles.warName }>{ war.name }</span> is still being prepared ‍🛠️
      </p>
      <p className={ styles.text }>
        After we finish preparing this war, you will be able to upload your memes to it.
      </p>
      <p className={ styles.text }>
        Each meme that you upload to the war has to be approved so others could see and rate it.
      </p>
    </div>
  );
}
