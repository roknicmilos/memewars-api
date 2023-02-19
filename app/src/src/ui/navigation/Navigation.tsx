import React from "react";
import styles from "./Navigation.module.scss";
import { UserMenu } from "./user-menu/UserMenu";


export function Navigation() {
  return (
    <nav className={ styles.navigation }>
      <UserMenu/>
    </nav>
  );
}
