import React, { useEffect, useState } from "react";
import { Loader } from "../../loader/Loader";
import { Navigate, useParams } from "react-router-dom";
import { useAuth } from "../../../context/authContext";
import { warService } from "../../../services/warService";
import { War, WarPhases } from "../../../models/war";
import { FinishedWar } from "./finished-war/FinishedWar";

export function WarDetailsPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ war, setWar ] = useState<War | null>(null);
  const { user } = useAuth();
  const { warID } = useParams();

  useEffect(() => {
    async function fetchWar() {
      const war = await warService.getWar(Number(warID));
      setWar(war);
      setIsLoading(false);
    }

    if (!user) {
      setIsLoading(false);
    } else if (isLoading) {
      fetchWar();
    }
  }, [ war ]);

  if (isLoading) return <Loader/>;

  if (!user) return <Navigate to="/login" replace/>;

  if (war && war.phase === WarPhases.finished) return <FinishedWar war={ war }/>;

  // TODO: render other war phases

  return <div>Invalid war</div>; // TODO: style
}
