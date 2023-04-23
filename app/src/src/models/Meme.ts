export interface Meme {
  id: number;
  image: string;
  war: number;
  user: number;
  approval_status: ApprovalStatus;
  total_score: number;
  vote_count: number;
  created: string;
  modified: string;
}

export enum ApprovalStatus {
  pending = "pending",
  approved = "approved",
  rejected = "rejected",
}
