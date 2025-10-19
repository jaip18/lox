import { TrendingUp, TrendingDown } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface BetCardProps {
  playerName: string;
  team: string;
  opponent: string;
  betType: string;
  line: number;
  confidence: number;
  gameDate: string;
  outcome?: "win" | "loss" | null;
}

export const BetCard = ({
  playerName,
  team,
  opponent,
  betType,
  line,
  confidence,
  gameDate,
  outcome,
}: BetCardProps) => {
  const confidenceColor =
    confidence >= 80
      ? "text-success"
      : confidence >= 60
      ? "text-accent"
      : "text-muted-foreground";

  return (
    <Card className="group relative overflow-hidden border-border bg-gradient-card p-4 transition-all hover:shadow-card hover:scale-[1.02]">
      <div className="absolute inset-0 bg-gradient-primary opacity-0 transition-opacity group-hover:opacity-5" />
      
      <div className="relative flex items-center gap-4">
        <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-secondary text-2xl font-bold">
          {playerName.split(" ").map(n => n[0]).join("")}
        </div>

        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-foreground">{playerName}</h3>
            <Badge variant="outline" className="text-xs">
              {team}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground">vs {opponent}</p>
          <div className="mt-1 flex items-center gap-2">
            <span className="text-sm font-medium text-accent">
              {betType} {line}
            </span>
            <span className="text-xs text-muted-foreground">{gameDate}</span>
          </div>
        </div>

        <div className="flex flex-col items-end gap-2">
          <div className={`text-3xl font-bold ${confidenceColor}`}>
            {confidence}%
          </div>
          {outcome && (
            <Badge
              variant={outcome === "win" ? "default" : "destructive"}
              className="gap-1"
            >
              {outcome === "win" ? (
                <TrendingUp className="h-3 w-3" />
              ) : (
                <TrendingDown className="h-3 w-3" />
              )}
              {outcome === "win" ? "Won" : "Lost"}
            </Badge>
          )}
        </div>
      </div>
    </Card>
  );
};
