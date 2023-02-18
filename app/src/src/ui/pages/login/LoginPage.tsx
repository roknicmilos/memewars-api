import React from "react";
import styles from "./LoginPage.module.scss";
import googleColoredLogo from "../../../assets/google-colored.svg";


export function LoginPage() {
  return (
    <div className={ styles.container }>
      <h1 className={ styles.title }>Welcome to the Meme Wars</h1>
      <button className={ styles.googleLoginButton }>
        <img src={ googleColoredLogo } alt="google-colored-logo"/>
        <span className={ styles.googleLoginButtonLabel }>Login with Google</span>
      </button>
    </div>
  );
}
