export interface War {
  id: number;
  name: string;
  phase: WarPhases;
  requires_meme_approval: boolean;
  created: string;
  modified: string;
}

export enum WarPhases {
  preparation = "preparation",
  submission = "submission",
  voting = "voting",
  finished = "finished",
}
