import React from "react";
import styles from "./Navigation.module.scss";
import { UserMenu } from "./user-menu/UserMenu";
import { useAuth } from "../../context/authContext";


export function Navigation() {
  const { user } = useAuth();

  return (
    <nav className={ styles.navigation }>
      <div className={ styles.container }>
        { user && <UserMenu/> }
      </div>
    </nav>
  );
}
