export interface Meme {
  id: number;
  image: string;
  war: number;
  user: number;
  approval_status: ApprovalStatus;
  created: string;
  modified: string;
}

export enum ApprovalStatus {
  pending = "pending",
  approved = "approved",
  rejected = "rejected",
}
