import React, { useEffect, useState } from "react";
import { Navigate, useSearchParams } from "react-router-dom";
import { UserFriendlyError } from "../../../userFriendlyError";
import { useAuth } from "../../../context/authContext";
import { userService } from "../../../services/userService";
import { Loader } from "../../loader/Loader";


export function IndexPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ searchParams, setSearchParams ] = useSearchParams();
  const [ isAuthenticated, setIsAuthenticated ] = useState<boolean>(false);
  const { user, saveUser } = useAuth();

  useEffect(() => {
    setIsAuthenticated(!!user);
    if (!user && searchParams.has("has_authenticated_successfully")) {
      handleLoginCallback();
    }
    setIsLoading(false);
  }, [ user ]);

  function handleLoginCallback(): void {
    const hasAuthenticatedSuccessfully = searchParams.get("has_authenticated_successfully")?.toLowerCase() === "true";
    if (hasAuthenticatedSuccessfully) {
      const user = userService.mapURLQueryParamsToUser(searchParams);
      saveUser(user);
      setSearchParams({});
    } else {
      throw new UserFriendlyError("Looks like there was a login error.");
    }
  }

  if (isLoading) return <Loader/>;

  return <Navigate to={ isAuthenticated ? "/wars" : "/login" } replace/>;
}
