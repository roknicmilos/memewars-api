import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../../../context/authContext";
import styles from "./LoginErrorPage.module.scss";

export function LoginErrorPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ errorCode, setErrorCode ] = useState<string>();
  const [ searchParams ] = useSearchParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isLoading) {
      user && navigate("/wars");
      searchParams.has("code") && setErrorCode(searchParams.get("code")!);
      setIsLoading(false);
    }
  }, [ isLoading, user ]);

  return (
    <div className={ styles.container }>
      <h2 className={ styles.title }>Login Error</h2>
      <p className={ styles.errorMessage }>
        { errorCode == "forbidden_email" ? (
          "That email address is not allowed 🥲"
        ) : (
          "Looks like there was a login error 🥲"
        ) }
      </p>
      <a className={ styles.button } href="/login">Back to login</a>
    </div>
  );
}
