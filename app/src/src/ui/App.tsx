import React from "react";
import { router } from "../router";
import { RouterProvider } from "react-router-dom";
import { Navigation } from "./components/navigation/Navigation";
import styles from "./main.module.scss";

export function App() {
  return (
    <>
      <Navigation/>
      <div className={ styles.content }>
        <RouterProvider router={ router }/>
      </div>
    </>
  );
}
