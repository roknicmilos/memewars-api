import React from "react";
import styles from "./LoginPage.module.scss";
import { authService } from "../../../services/authService";
import { GoogleColoredSVG } from "../../svg/GoogleColoredSVG";


export function LoginPage() {
  return (
    <div className={ styles.container }>
      <h1 className={ styles.title }>Welcome to the Meme Wars</h1>
      <a className={ styles.googleLoginButton } href={ authService.getLoginUrl() }>
        <GoogleColoredSVG height="40px" width="40px"/>
        <span className={ styles.googleLoginButtonLabel }>Login with Google</span>
      </a>
    </div>
  );
}
