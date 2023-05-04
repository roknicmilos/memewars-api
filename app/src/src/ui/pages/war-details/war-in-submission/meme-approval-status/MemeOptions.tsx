import React, { CSSProperties, MouseEvent, useState } from "react";
import { ApprovalStatus } from "../../../../../models/Meme";
import styles from "./MemeOptions.module.scss";
import awaitingSVG from "../../../../../assets/awaiting.svg";
import approvedSVG from "../../../../../assets/approved.svg";
import rejectedSVG from "../../../../../assets/rejected.svg";
import trashSVG from "../../../../../assets/trash.svg";
import { Modal } from "../../../../components/modal/Modal";

interface MemeOptionsProps {
  approvalStatus: ApprovalStatus;
  isExpanded: boolean;
  onStatusClick(): void;
  onDeleteMeme(): Promise<void>;
}

export function MemeOptions({ approvalStatus, isExpanded, onStatusClick, onDeleteMeme }: MemeOptionsProps) {
  const [ hasOpenedDeleteModal, setHasOpenedDeleteModal ] = useState<boolean>(false);
  const memeOptionsContent = getMemeOptionsContent(approvalStatus);

  async function handleDeleteMeme(event: MouseEvent) {
    event.preventDefault();
    try {
      await onDeleteMeme();
    } finally {
      setHasOpenedDeleteModal(false);
    }
  }

  return (
    <div className={ isExpanded ? styles.optionsOpened : styles.options }>
      <div className={ styles.status } onClick={ onStatusClick }>
        <img className={ styles.statusIcon } src={ memeOptionsContent.imageSrc } alt={ memeOptionsContent.imageAlt }/>
        <p className={ styles.statusText } style={ memeOptionsContent.textStyle }>{ memeOptionsContent.text }</p>
      </div>
      <div className={ styles.deleteButton } onClick={ () => setHasOpenedDeleteModal(true) }>
        <img className={ styles.deleteIcon } src={ trashSVG } alt="trash"/>
      </div>
      <Modal onClose={ () => setHasOpenedDeleteModal(false) } isOpened={ hasOpenedDeleteModal }>
        <div className={ styles.deleteModalContent }>
          <p>Not proud of this meme?</p>
          <p>Maybe it's fot the best if no one else sees it 🤫</p>
          <p>Can I delete it? Say "yes"!</p>
          <div className={ styles.deleteModalButtons }>
            <button className={ styles.abortDeletionButton } onClick={ () => setHasOpenedDeleteModal(false) }>
              <p>NO!</p><span className={ styles.emoji }>😡</span>
            </button>
            <button className={ styles.confirmDeletionButton } onClick={ handleDeleteMeme }>
              <p>Yeah</p><span className={ styles.emoji }>😒</span>
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

interface MemeOptionsContent {
  textStyle: CSSProperties;
  text: string;
  imageSrc: string;
  imageAlt: string;
}

function getMemeOptionsContent(approvalStatus: ApprovalStatus): MemeOptionsContent {
  switch (approvalStatus) {
    case ApprovalStatus.pending:
      return {
        textStyle: { color: "royalblue" },
        text: "Awaiting approval",
        imageSrc: awaitingSVG,
        imageAlt: "awaiting",
      };
    case ApprovalStatus.approved:
      return {
        textStyle: { color: "green" },
        text: "Approved",
        imageSrc: approvedSVG,
        imageAlt: "approved",
      };
    case ApprovalStatus.rejected:
      return {
        textStyle: { color: "red" },
        text: "Rejected",
        imageSrc: rejectedSVG,
        imageAlt: "rejected",
      };
  }
}