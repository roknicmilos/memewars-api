import React from "react";
import styles from "./WarInSubmissionMeme.module.scss";
import { Meme } from "../../../../../models/meme";
import { MemeApprovalStatus } from "../meme-approval-status/MemeApprovalStatus";

interface WarInSubmissionMemeProps {
  meme: Meme;
  displayApprovalStatus?: boolean;
}

export function WarInSubmissionMeme({ meme, displayApprovalStatus }: WarInSubmissionMemeProps) {
  return (
    <div className={ styles.meme }>
      { displayApprovalStatus && <MemeApprovalStatus approvalStatus={ meme.approval_status }/> }
      <img className={ styles.memeImage } src={ meme.image } alt="meme"/>
    </div>
  );
}
