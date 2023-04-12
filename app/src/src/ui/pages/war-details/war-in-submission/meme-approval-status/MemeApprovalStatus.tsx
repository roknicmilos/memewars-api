import React from "react";
import { ApprovalStatus } from "../../../../../models/meme";
import styles from "./MemeApprovalStatus.module.scss";
import awaitingSVG from "../../../../../assets/awaiting.svg";
import approvedSVG from "../../../../../assets/approved.svg";
import rejectedSVG from "../../../../../assets/rejected.svg";

interface MemeApprovalStatusProps {
  approvalStatus: ApprovalStatus;
}

export function MemeApprovalStatus({ approvalStatus }: MemeApprovalStatusProps) {
  switch (approvalStatus) {
    case ApprovalStatus.pending:
      return (
        <div className={ styles.statusCardAwaiting }>
          <p className={ styles.statusText }>Awaiting approval</p>
          <img className={ styles.statusIcon } src={ awaitingSVG } alt="awaiting"/>
        </div>
      );
    case ApprovalStatus.approved:
      return (
        <div className={ styles.statusCardApproved }>
          <p className={ styles.statusText }>Approved</p>
          <img className={ styles.statusIcon } src={ approvedSVG } alt="approved"/>
        </div>
      );
    case ApprovalStatus.rejected:
      return (
        <div className={ styles.statusCardRejected }>
          <p className={ styles.statusText }>Rejected</p>
          <img className={ styles.statusIcon } src={ rejectedSVG } alt="rejected"/>
        </div>
      );
  }
}
