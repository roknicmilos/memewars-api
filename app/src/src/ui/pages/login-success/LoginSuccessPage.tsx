import React, { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../../../context/authContext";
import { userService } from "../../../services/userService";

/**
 * Purpose of this component is not to show any content (to render anything).
 * Instead, it only redirects to an appropriate page.
 */
export function LoginSuccessPage() {
  const [ searchParams ] = useSearchParams();
  const { user, saveUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/login");
    }
    saveUser(userService.mapURLQueryParamsToUser(searchParams));
    navigate("/wars");

  }, [ user ]);

  return <></>;

}
