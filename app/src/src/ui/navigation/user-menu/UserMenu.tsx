import React, { useState } from "react";
import styles from "./UserMenu.module.scss";
import dropdownCarrotSVG from "../../../assets/dropdown-carrot.svg";
import avatarSVG from "../../../assets/avatar.svg";
import { useAuth } from "../../../context/authContext";


export function UserMenu() {
  const { user, clearUser } = useAuth();
  const [ isOpened, setIsOpened ] = useState<boolean>(false);

  function toggleUserMenu(): void {
    setIsOpened(!isOpened);
  }

  return (
    <div className={ styles.userMenu }>
      <div className={ styles.avatarButton } onClick={ toggleUserMenu }>
        <img
          className={ styles.profileImage }
          src={ user?.imageURL ? user.imageURL : avatarSVG }
          alt="profile image"
          onError={ ({ currentTarget }) => {
            currentTarget.src = avatarSVG;
          } }
        />
        <img
          className={ styles.dropdownCarrot }
          style={ isOpened ? { transform: "rotate(180deg)" } : {} }
          src={ dropdownCarrotSVG }
          alt="dropdown carrot"
        />
      </div>
      { isOpened && (
        <div className={ styles.userMenuItems }>
          <div className={ styles.userMenuItem } onClick={ clearUser }>LOGOUT</div>
        </div>
      ) }
    </div>
  );
}
