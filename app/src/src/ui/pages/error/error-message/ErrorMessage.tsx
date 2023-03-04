import { UserFriendlyError } from "../../../../userFriendlyError";
import React from "react";

interface ErrorMessageProps {
  error: any;
}

export function ErrorMessage({ error }: ErrorMessageProps) {
  if (error.status === 404) {
    return <p>We couldn't find this page 😱</p>;
  }
  if (error instanceof UserFriendlyError) {
    return <p>{ error.message }</p>;
  }
  return <p>Sorry, an unexpected error has occurred 🙃</p>;
}
