import styles from "./WarsCard.module.scss";
import React from "react";
import { War } from "../../../../models/war";

interface WarCardProps {
  war: War;
}

export function WarCard({ war }: WarCardProps) {
  const phaseClasses = [ styles.warPhase, styles[`${ war.phase }Phase`] ].join(" ");
  return (
    <div key={ war.id } className={ styles.warCard }>
      <p className={ styles.warName }>{ war.name }</p>
      <p className={ phaseClasses }>{ war.phase }</p>
    </div>
  );
}
