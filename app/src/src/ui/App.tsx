import React from "react";
import { router } from "../router";
import { RouterProvider } from "react-router-dom";
import { Navigation } from "./navigation/Navigation";


export function App() {
  return (
    <>
      <Navigation/>
      <RouterProvider router={ router }/>
    </>
  );
}