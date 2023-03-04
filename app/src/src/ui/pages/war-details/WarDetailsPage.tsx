import React from "react";
import { useLoaderData } from "react-router-dom";
import { War, WarPhases } from "../../../models/war";
import { FinishedWar } from "./finished-war/FinishedWar";

export function WarDetailsPage() {
  const war = useLoaderData() as War;

  if (war && war.phase === WarPhases.finished) return <FinishedWar war={ war }/>;

  // TODO: render other war phases

  return <div>Invalid war</div>; // TODO: style
}
