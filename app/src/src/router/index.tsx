import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { ErrorPage } from "../ui/pages/error/ErrorPage";
import { IndexPage } from "../ui/pages/index/IndexPage";
import { LoginPage } from "../ui/pages/login/LoginPage";
import { LoginErrorPage } from "../ui/pages/login-error/LoginErrorPage";
import { LoginSuccessPage } from "../ui/pages/login-success/LoginSuccessPage";
import { WarListPage } from "../ui/pages/war-list/WarListPage";
import { WarDetailsPage } from "../ui/pages/war-details/WarDetailsPage";
import { warDetailsLoader, warListLoader } from "./loaders/warLoaders";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage/>,
    errorElement: <ErrorPage/>,
    children: [
      {
        path: "login",
        element: <LoginPage/>,
      },
      {
        path: "login-error",
        element: <LoginErrorPage/>,
      },
      {
        path: "login-success",
        element: <LoginSuccessPage/>,
      },
      {
        path: "wars",
        element: <WarListPage/>,
        loader: warListLoader,
      },
      {
        path: "wars/:warID",
        element: <WarDetailsPage/>,
        loader: warDetailsLoader,
      },
    ],
  },
]);
