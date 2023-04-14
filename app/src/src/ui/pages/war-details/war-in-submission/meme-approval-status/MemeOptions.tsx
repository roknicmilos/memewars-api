import React, { CSSProperties } from "react";
import { ApprovalStatus } from "../../../../../models/meme";
import styles from "./MemeOptions.module.scss";
import awaitingSVG from "../../../../../assets/awaiting.svg";
import approvedSVG from "../../../../../assets/approved.svg";
import rejectedSVG from "../../../../../assets/rejected.svg";
import trashSVG from "../../../../../assets/trash.svg";

interface MemeOptionsProps {
  approvalStatus: ApprovalStatus;
  isExpanded?: boolean;
  onStatusClick?(): void;
}

export function MemeOptions({ approvalStatus, isExpanded, onStatusClick }: MemeOptionsProps) {
  const memeOptionsContent = getMemeOptionsContent(approvalStatus);
  return (
    <div className={ isExpanded ? styles.optionsOpened : styles.options }>
      <div className={ styles.status } onClick={ onStatusClick }>
        <img className={ styles.statusIcon } src={ memeOptionsContent.imageSrc } alt={ memeOptionsContent.imageAlt }/>
        <p className={ styles.statusText } style={ memeOptionsContent.textStyle }>{ memeOptionsContent.text }</p>
      </div>
      <div className={ styles.deleteButton }>
        <img className={ styles.deleteIcon } src={ trashSVG } alt="trash"/>
      </div>
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