import React, { useEffect, useState } from "react";
import styles from "./WarsListPage.module.scss";
import { War } from "../../../models/war";
import { warService } from "../../../services/warService";
import { WarCard } from "./war-card/WarCard";
import { Loader } from "../../loader/Loader";
import { useAuth } from "../../../context/authContext";
import { Navigate } from "react-router-dom";


export function WarsListPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ wars, setWars ] = useState<War[]>([]);
  const [ containerStyle, setContainerStyle ] = useState<object>({});
  const { user } = useAuth();

  useEffect(() => {
    async function fetchWars() {
      const wars = await warService.getWars();
      if (wars.length < 3) {
        setContainerStyle({ justifyContent: "center" });
      }
      setWars(wars);
      setIsLoading(false);
    }

    if (!user) {
      setIsLoading(false);
    } else if (isLoading) {
      fetchWars();
    }
  }, [ wars ]);

  if (isLoading) return <Loader/>;

  if (!user) return <Navigate to="/login" replace/>;

  return (
    <div className={ styles.container } style={ containerStyle }>
      { wars && wars.map(war => (<WarCard key={ war.id } war={ war }/>)) }
    </div>
  );
}
