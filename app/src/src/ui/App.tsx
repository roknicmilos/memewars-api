import React from "react";
import { router } from "../router";
import { RouterProvider } from "react-router-dom";
import { useAuth } from "../context/authContext";
import { Navigation } from "./navigation/Navigation";


export function App() {
  const { user } = useAuth();

  return (
    <>
      { user && <Navigation/> }
      <RouterProvider router={ router }/>
    </>
  );
}
