import React from "react";
import { useLoaderData } from "react-router-dom";
import { War, WarPhases } from "../../../models/War";
import { UserFriendlyError } from "../../../userFriendlyError";
import { FinishedWar } from "./finished-war/FinishedWar";
import { WarInPreparation } from "./war-in-preparation/WarInPreparation";
import { WarInSubmission } from "./war-in-submission/WarInSubmission";

export function WarDetailsPage() {
  const war = useLoaderData() as War;


  switch (war?.phase) {
    case WarPhases.finished:
      return <FinishedWar war={ war }/>;
    case WarPhases.preparation:
      return <WarInPreparation war={ war }/>;
    case WarPhases.submission:
      return <WarInSubmission war={ war }/>;
  }

  // TODO: render other war phases

  throw new UserFriendlyError("We don't know what kind of a war this is 😬");
}
