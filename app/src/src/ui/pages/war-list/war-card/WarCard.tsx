import styles from "./WarCard.module.scss";
import React from "react";
import { War } from "../../../../models/War";
import { Link } from "react-router-dom";

interface WarCardProps {
  war: War;
}

export function WarCard({ war }: WarCardProps) {
  const phaseClasses = [ styles.warPhase, styles[`${ war.phase }Phase`] ].join(" ");

  return (
    <Link key={ war.id } className={ styles.warCard } to={ `/wars/${ war.id }` }>
      <span className={ styles.warName }>{ war.name }</span>
      <span className={ phaseClasses }>{ war.phase }</span>
    </Link>
  );
}
