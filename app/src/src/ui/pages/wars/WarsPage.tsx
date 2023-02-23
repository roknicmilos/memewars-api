import React, { useEffect, useState } from "react";
import styles from "./WarsPage.module.scss";
import { War } from "../../../models/war";
import { warService } from "../../../services/warService";
import { WarCard } from "./war-card/WarCard";


export function WarsPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ wars, setWars ] = useState<War[]>([]);
  const [ containerStyle, setContainerStyle ] = useState<object>({});

  useEffect(() => {
    async function fetchWars() {
      const wars = await warService.getWars();
      if (wars.length < 3) {
        setContainerStyle({ justifyContent: "center" });
      }
      setWars(wars);
      setIsLoading(false);
    }

    if (isLoading) {
      fetchWars();
    }
  }, [ wars ]);


  return (
    <div className={ styles.container } style={ containerStyle }>
      { wars && wars.map(war => (<WarCard key={ war.id } war={ war }/>)) }
    </div>
  );
}
