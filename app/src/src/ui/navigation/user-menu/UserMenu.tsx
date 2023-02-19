import React, { useState } from "react";
import styles from "./UserMenu.module.scss";
import avatarSVG from "../../../assets/avatar.svg";
import { useAuth } from "../../../context/authContext";
import { Modal } from "../../modal/Modal";


export function UserMenu() {
  const { user, clearUser } = useAuth();
  const [ isOpened, setIsOpened ] = useState<boolean>(false);

  return (
    <>
      <div className={ styles.avatarButton } onClick={ () => setIsOpened(true) }>
        <img
          className={ styles.profileImage }
          src={ user?.imageURL ? user.imageURL : avatarSVG }
          alt="profile image"
          onError={ ({ currentTarget }) => {
            currentTarget.src = avatarSVG;
          } }
        />
      </div>
      <Modal isOpened={ isOpened } onClose={ () => setIsOpened(false) }>
        <div className={ styles.modalText }>
          <p>Had enough?</p>
          <p>
            Go scroll some Instagram or Facebook a bit so that you can remind
            yourself that this is a much better waist of your time...
          </p>
        </div>
        <div className={ styles.logoutButton } onClick={ clearUser }>LOGOUT</div>
      </Modal>
    </>
  );
}
