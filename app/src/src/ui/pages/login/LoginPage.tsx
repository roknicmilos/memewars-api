import React, { useEffect } from "react";
import styles from "./LoginPage.module.scss";
import { authService } from "../../../services/authService";
import { useAuth } from "../../../context/authContext";
import { useNavigate } from "react-router-dom";
import { useLoader } from "../../../context/loaderContext";
import googleDarkSVG from "./../../../assets/googleDark.svg";
import googleWhiteSVG from "./../../../assets/googleWhite.svg";


export function LoginPage() {
  const { setIsLoading } = useLoader();
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/wars");
    }
  }, [ user ]);

  function redirectToLoginURL(): void {
    setIsLoading(true);
    window.location.href = authService.getLoginUrl();
  }

  return (
    <div className={ styles.container }>
      { !user && (
        <>
          <h1 className={ styles.title }>Welcome to the Meme Wars</h1>
          <div className={ styles.button } onClick={ redirectToLoginURL }>
            <img className={ styles.darkGoogleIcon } src={ googleDarkSVG } alt="dark google icon"/>
            <img className={ styles.whiteGoogleIcon } src={ googleWhiteSVG } alt="white google icon"/>
            <span className={ styles.buttonLabel }>Login with Google</span>
          </div>
        </>
      ) }
    </div>
  );
}
