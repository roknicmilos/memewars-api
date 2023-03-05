import React from "react";
import { useLoaderData } from "react-router-dom";
import { War, WarPhases } from "../../../models/war";
import { FinishedWar } from "./finished-war/FinishedWar";
import { UserFriendlyError } from "../../../userFriendlyError";
import { WarInPreparation } from "./war-in-preparation/WarInPreparation";

export function WarDetailsPage() {
  const war = useLoaderData() as War;


  switch (war?.phase) {
    case WarPhases.finished:
      return <FinishedWar war={ war }/>;
    case WarPhases.preparation:
      return <WarInPreparation war={ war }/>;
  }

  // TODO: render other war phases

  throw new UserFriendlyError("We don't know what kind of a war this is 😬");
}
