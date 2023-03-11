import React from "react";
import styles from "./Navigation.module.scss";
import burgerSVG from "../../../assets/burger.svg";
import { UserMenu } from "./user-menu/UserMenu";
import { useAuth } from "../../../context/authContext";


export function Navigation() {
  const { user } = useAuth();

  return (
    <nav className={ styles.navigation }>
      <div className={ styles.container }>
        <a className={ styles.homeButton } href={ "/" }>
          <img src={ burgerSVG } alt="burger svg"/>
        </a>
        { user && <UserMenu/> }
      </div>
    </nav>
  );
}
