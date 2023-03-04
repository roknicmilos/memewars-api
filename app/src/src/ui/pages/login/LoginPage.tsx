import React, { useEffect } from "react";
import styles from "./LoginPage.module.scss";
import { authService } from "../../../services/authService";
import { useAuth } from "../../../context/authContext";
import { useNavigate } from "react-router-dom";
import { useLoader } from "../../../context/loaderContext";
import { GoogleColoredSVG } from "../../svg/GoogleColoredSVG";


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
            <GoogleColoredSVG height="40px" width="40px"/>
            <span className={ styles.buttonLabel }>Login with Google</span>
          </div>
        </>
      ) }
    </div>
  );
}
