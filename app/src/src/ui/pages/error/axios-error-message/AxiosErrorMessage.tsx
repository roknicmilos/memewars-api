import { AxiosError } from "axios";
import React from "react";

interface AxiosErrorMessageProps {
  error: AxiosError;
  isAuthenticated: boolean;
}

function Message401({ isAuthenticated }: { isAuthenticated: boolean }) {
  return (
    <>
      <p>We don't know who you are 🧐</p>
      { isAuthenticated ? (
        <>
          <p>Try to logout and log in again.</p>
          <p>Should work 🤞</p>
        </>
      ) : (
        <p>In order to see what's no this page, you'll have to log in.</p>
      ) }
    </>
  );

}

export function AxiosErrorMessage({ error, isAuthenticated }: AxiosErrorMessageProps) {
  if (error.response?.status === 401) {
    return <Message401 isAuthenticated={ isAuthenticated }/>;
  }
  if (error.response?.status === 404) {
    return <p>We couldn't find this page 😱</p>;
  }
  return <p>Sorry, an unexpected error has occurred 🙃</p>;
}
