import React, { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate, useSearchParams } from "react-router-dom";
import { UserFriendlyError } from "../../../userFriendlyError";
import { useAuth } from "../../../context/authContext";
import { userService } from "../../../services/userService";

export function IndexPage() {
  const [ isLoading, setIsLoading ] = useState<boolean>(true);
  const [ searchParams ] = useSearchParams();
  const { user, saveUser } = useAuth();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  useEffect(() => {
    if (pathname === "/" && isLoading) {
      if (user) {
        navigate("/wars");
      } else {
        if (searchParams.has("has_authenticated_successfully")) {
          handleLoginCallback();
        } else {
          navigate("/login");
        }
      }
      setIsLoading(false);
    }
  }, [ isLoading, user ]);

  function handleLoginCallback(): void {
    if (searchParams.get("has_authenticated_successfully")?.toLowerCase() === "true") {
      const user = userService.mapURLQueryParamsToUser(searchParams);
      saveUser(user);
      navigate("/wars");
    } else {
      // TODO: remove URL query params without reloading before raising an error
      if (searchParams.get("code") == "forbidden_email") {
        throw new UserFriendlyError("That email address is not allowed 🥲");
      }
      throw new UserFriendlyError("Looks like there was a login error 🥲");
    }
  }

  return <Outlet/>;
}
