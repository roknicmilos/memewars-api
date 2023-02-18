import styles from "./ErrorPage.module.scss";
import React from "react";
import { useRouteError } from "react-router-dom";
import { UserFriendlyError } from "../../../userFriendlyError";

export function ErrorPage() {
  const error: any = useRouteError();

  const getMessage = function (): string {
    if (error.status === 404) {
      return "We couldn't find this page";
    }
    if (error instanceof UserFriendlyError) {
      return error.message;
    }
    return "Sorry, an unexpected error has occurred.";
  };

  return (
    <div className={ styles.container }>
      <h1>Oops!</h1>
      <p>{ getMessage() }</p>
    </div>
  );
}
