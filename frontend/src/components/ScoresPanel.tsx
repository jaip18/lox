import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Trophy } from "lucide-react";

interface Game {
  id: string;
  homeTeam: string;
  awayTeam: string;
  homeScore: number;
  awayScore: number;
  status: string;
  quarter?: string;
}

const mockGames: Game[] = [
  { id: "1", homeTeam: "LAL", awayTeam: "GSW", homeScore: 112, awayScore: 108, status: "Final" },
  { id: "2", homeTeam: "BOS", awayTeam: "MIA", homeScore: 98, awayScore: 95, status: "Q4 2:35" },
  { id: "3", homeTeam: "PHX", awayTeam: "DAL", homeScore: 89, awayScore: 91, status: "Q3 8:12" },
  { id: "4", homeTeam: "MIL", awayTeam: "DEN", homeScore: 0, awayScore: 0, status: "7:30 PM" },
];

export const ScoresPanel = () => {
  return (
    <Card className="h-fit border-border bg-card p-6">
      <div className="mb-4 flex items-center gap-2">
        <Trophy className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-semibold">Live Scores</h2>
      </div>

      <div className="space-y-3">
        {mockGames.map((game) => (
          <div
            key={game.id}
            className="rounded-lg border border-border bg-secondary/50 p-3 transition-colors hover:bg-secondary"
          >
            <div className="mb-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-semibold">{game.awayTeam}</span>
                <span className="text-lg font-bold text-foreground">
                  {game.awayScore}
                </span>
              </div>
              {game.status === "Final" ? (
                <Badge variant="outline">Final</Badge>
              ) : game.status.includes("PM") ? (
                <Badge variant="secondary">{game.status}</Badge>
              ) : (
                <Badge variant="default" className="animate-pulse">
                  {game.status}
                </Badge>
              )}
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold">{game.homeTeam}</span>
              <span className="text-lg font-bold text-foreground">
                {game.homeScore}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
