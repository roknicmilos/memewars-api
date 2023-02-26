import React, { useEffect, useState } from "react";
import styles from "./WarsListPage.module.scss";
import { War } from "../../../models/war";
import { warService } from "../../../services/warService";
import { WarCard } from "./war-card/WarCard";
import { Loader } from "../../loader/Loader";


export function WarsListPage() {
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

  if (isLoading) return <Loader/>;

  return (
    <div className={ styles.container } style={ containerStyle }>
      { wars && wars.map(war => (<WarCard key={ war.id } war={ war }/>)) }
    </div>
  );
}
