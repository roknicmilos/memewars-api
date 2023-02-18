import React from "react";
import styles from "./LoginPage.module.scss";
import googleColoredLogo from "../../../assets/google-colored.svg";
import { authService } from "../../../services/authService";


export function LoginPage() {
  return (
    <div className={ styles.container }>
      <h1 className={ styles.title }>Welcome to the Meme Wars</h1>
      <a className={ styles.googleLoginButton } href={ authService.getLoginUrl() }>
        <img src={ googleColoredLogo } alt="google-colored-logo"/>
        <span className={ styles.googleLoginButtonLabel }>Login with Google</span>
      </a>
    </div>
  );
}
