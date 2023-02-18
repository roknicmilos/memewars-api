import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { WarsPage } from "../wars/WarsPage";
import { LoginPage } from "../login/LoginPage";
import { authService } from "../../../services/authService";
import { UserFriendlyError } from "../../../userFriendlyError";


export function HomePage() {
  const [ searchParams, setSearchParams ] = useSearchParams();
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ isAuthenticated, setIsAuthenticated ] = useState<boolean>(false);

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      setIsAuthenticated(true);
    } else if (searchParams.has("has_authenticated_successfully")) {
      handleLoginCallback();
    }
    setIsLoading(false);
  }, []);

  function handleLoginCallback(): void {
    const hasAuthenticatedSuccessfully = searchParams.get("has_authenticated_successfully")?.toLowerCase() === "true";
    if (hasAuthenticatedSuccessfully) {
      const user = authService.mapURLQueryParamsToUser(searchParams);
      localStorage.setItem("user", JSON.stringify(user));
      setSearchParams({});
    } else {
      throw new UserFriendlyError("Looks like there was a login error.");
    }
  }

  if (isLoading) return <div>loading...</div>;

  return isAuthenticated ? <WarsPage/> : <LoginPage/>;
}
