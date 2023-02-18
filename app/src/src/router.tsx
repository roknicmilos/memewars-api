import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { ErrorPage } from "./ui/pages/error/ErrorPage";
import { HomePage } from "./ui/pages/home/HomePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage/>,
    errorElement: <ErrorPage/>,
  },
]);
