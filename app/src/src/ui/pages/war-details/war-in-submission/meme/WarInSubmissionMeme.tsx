import React, { useState } from "react";
import styles from "./WarInSubmissionMeme.module.scss";
import { Meme } from "../../../../../models/Meme";
import { MemeOptions } from "../meme-approval-status/MemeOptions";

interface WarInSubmissionMemeProps {
  meme: Meme;
  displayApprovalStatus?: boolean;
  onDelete(): Promise<void>;
}

export function WarInSubmissionMeme({ meme, displayApprovalStatus, onDelete }: WarInSubmissionMemeProps) {
  const [ isShowingDetails, setIsShowingDetails ] = useState<boolean>(false);

  return (
    <div className={ styles.meme }>
      { displayApprovalStatus && (
        <MemeOptions
          approvalStatus={ meme.approval_status }
          isExpanded={ isShowingDetails }
          onStatusClick={ () => setIsShowingDetails(!isShowingDetails) }
          onDeleteMeme={ onDelete }
        />
      ) }
      <img
        className={ styles.memeImage }
        src={ meme.image }
        alt="meme"
        onClick={ () => setIsShowingDetails(!isShowingDetails) }
      />
    </div>
  );
}
