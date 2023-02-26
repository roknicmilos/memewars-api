import React, { useState } from "react";
import styles from "./LoginPage.module.scss";
import { authService } from "../../../services/authService";
import { GoogleColoredSVG } from "../../svg/GoogleColoredSVG";
import { Loader } from "../../loader/Loader";


export function LoginPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(false);

  function redirectToLoginURL(): void {
    setIsLoading(true);
    window.location.href = authService.getLoginUrl();
  }

  if (isLoading) return <Loader/>;

  return (
    <div className={ styles.container }>
      <h1 className={ styles.title }>Welcome to the Meme Wars</h1>
      <div className={ styles.button } onClick={ redirectToLoginURL }>
        <GoogleColoredSVG height="40px" width="40px"/>
        <span className={ styles.buttonLabel }>Login with Google</span>
      </div>
    </div>
  );
}
