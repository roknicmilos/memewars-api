import React, { MouseEvent } from "react";
import styles from "./Modal.module.scss";
import { CloseSVG } from "../svg/CloseSVG";


interface ModalProps {
  children?: JSX.Element | JSX.Element[];
  isOpened?: boolean;

  onClose(): void;
}

export function Modal({ children, isOpened, onClose }: ModalProps) {
  if (!isOpened) return null;

  function handleBackgroundClicked(event: MouseEvent<HTMLDivElement>): void {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  return (
    <div className={ styles.modalBackground } onClick={ handleBackgroundClicked }>
      <div className={ styles.modal }>
        <div className={ styles.closeButton } onClick={ onClose }>
          <CloseSVG/>
        </div>
        { children }
      </div>
    </div>
  );
}
