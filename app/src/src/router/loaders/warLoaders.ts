import { War } from "../../models/War";
import { warService } from "../../services/warService";

export async function warListLoader(): Promise<War[]> {
  return warService.getWars();
}

export async function warDetailsLoader({ params }: any): Promise<War> {
  return warService.getWar(params.warID);
}
