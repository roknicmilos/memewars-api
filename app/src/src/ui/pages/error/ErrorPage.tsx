import styles from "./ErrorPage.module.scss";
import React from "react";
import { useRouteError } from "react-router-dom";
import { useAuth } from "../../../context/authContext";
import { ErrorMessage } from "./error-message/ErrorMessage";
import { AxiosError } from "axios";
import { AxiosErrorMessage } from "./axios-error-message/AxiosErrorMessage";

export function ErrorPage() {
  const error: any = useRouteError();
  const { user } = useAuth();

  return (
    <div className={ styles.container }>
      <h1 className={ styles.title }>Oops</h1>
      <div className={ styles.message }>
        { error instanceof AxiosError ? (
          <AxiosErrorMessage error={ error } isAuthenticated={ !!user }/>
        ) : (
          <ErrorMessage error={ error }/>
        ) }
      </div>
      { !user && <a className={ styles.button } href="/login">Login</a> }
      <a className={ styles.button } href="/">Take me home</a>
    </div>
  );
}
