import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { ErrorPage } from "./ui/pages/error/ErrorPage";
import { IndexPage } from "./ui/pages/index/IndexPage";
import { WarsListPage } from "./ui/pages/war-list/WarsListPage";
import { LoginPage } from "./ui/pages/login/LoginPage";
import { WarDetailsPage } from "./ui/pages/war-details/WarDetailsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage/>,
    errorElement: <ErrorPage/>,
  },
  {
    path: "/login",
    element: <LoginPage/>,
  },
  {
    path: "/wars",
    element: <WarsListPage/>,
  },
  {
    path: "/wars/:warID",
    element: <WarDetailsPage/>,
  },
]);
