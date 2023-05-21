import React, { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../../context/authContext";

export function IndexPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/") {
      navigate(user ? "/wars" : "/login");
    }
  }, [ user ]);

  return <Outlet/>;
}
