import React, { useState } from "react";
import styles from "./UserMenu.module.scss";
import avatarSVG from "../../../../assets/avatar.svg";
import { useAuth } from "../../../../context/authContext";
import { Modal } from "../../modal/Modal";
import { useLoader } from "../../../../context/loaderContext";

export function UserMenu() {
  const { setIsLoading } = useLoader();
  const { user, clearUser } = useAuth();
  const [ isOpened, setIsOpened ] = useState<boolean>(false);

  function logout() {
    setIsLoading(true);
    clearUser();
    window.location.href = "/";
  }

  return (
    <>
      <div className={ styles.avatarButton } onClick={ () => setIsOpened(true) }>
        <img
          className={ styles.profileImage }
          src={ user?.imageURL ? user.imageURL : avatarSVG }
          alt={ `profile image for ${ user?.firstName } ${ user?.lastName }` }
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
        <div className={ styles.button } onClick={ logout }>Logout</div>
      </Modal>
    </>
  );
}
