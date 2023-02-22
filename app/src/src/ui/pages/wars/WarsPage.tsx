import React, { useEffect, useState } from "react";
import styles from "./WarsPage.module.scss";
import { War } from "../../../models/war";
import { warService } from "../../../services/warService";


export function WarsPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ wars, setWars ] = useState<War[]>([]);

  useEffect(() => {
    async function fetchWars() {
      const wars = await warService.getWars();
      setWars(wars);
      setIsLoading(false);
    }

    if (isLoading) {
      fetchWars();
    }
  }, [ wars ]);

  return (
    <>
      <div className={ styles.container }>
        { wars && wars.map(war => {
          const phaseClasses = [ styles.warPhase, styles[`${ war.phase }Phase`] ].join(" ");
          return (
            <div key={ war.id } className={ styles.warCard }>
              <p className={ styles.warName }>{ war.name }</p>
              <p className={ phaseClasses }>{ war.phase }</p>
            </div>
          );
        }) }
      </div>
    </>
  );
}
