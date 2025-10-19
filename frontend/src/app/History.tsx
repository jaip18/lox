import { BetCard } from "@/components/BetCard";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TrendingUp, TrendingDown } from "lucide-react";

const mockHistoricalBets = [
  {
    playerName: "LeBron James",
    team: "LAL",
    opponent: "GSW",
    betType: "Over",
    line: 25.5,
    confidence: 91,
    gameDate: "Dec 25",
    outcome: "win" as const,
  },
  {
    playerName: "Kevin Durant",
    team: "PHX",
    opponent: "LAL",
    betType: "Over",
    line: 27.5,
    confidence: 85,
    gameDate: "Dec 24",
    outcome: "win" as const,
  },
  {
    playerName: "Damian Lillard",
    team: "MIL",
    opponent: "BOS",
    betType: "Over",
    line: 5.5,
    confidence: 78,
    gameDate: "Dec 23",
    outcome: "loss" as const,
  },
  {
    playerName: "Anthony Davis",
    team: "LAL",
    opponent: "DEN",
    betType: "Over",
    line: 11.5,
    confidence: 88,
    gameDate: "Dec 22",
    outcome: "win" as const,
  },
];

const History = () => {
  const wins = mockHistoricalBets.filter((b) => b.outcome === "win").length;
  const total = mockHistoricalBets.length;
  const winRate = ((wins / total) * 100).toFixed(1);

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
          Bet History
        </h1>
        <p className="text-muted-foreground">
          Track performance of past recommendations
        </p>
      </div>

      <div className="mb-8 grid gap-4 md:grid-cols-3">
        <Card className="border-border bg-gradient-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Bets</p>
              <p className="mt-1 text-3xl font-bold">{total}</p>
            </div>
            <TrendingUp className="h-8 w-8 text-primary" />
          </div>
        </Card>

        <Card className="border-border bg-gradient-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Win Rate</p>
              <p className="mt-1 text-3xl font-bold text-success">{winRate}%</p>
            </div>
            <TrendingUp className="h-8 w-8 text-success" />
          </div>
        </Card>

        <Card className="border-border bg-gradient-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg Confidence</p>
              <p className="mt-1 text-3xl font-bold text-accent">85.5%</p>
            </div>
            <TrendingDown className="h-8 w-8 text-accent" />
          </div>
        </Card>
      </div>

      <Tabs defaultValue="all" className="space-y-6">
        <TabsList>
          <TabsTrigger value="all">All Bets</TabsTrigger>
          <TabsTrigger value="wins">Wins</TabsTrigger>
          <TabsTrigger value="losses">Losses</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {mockHistoricalBets.map((bet, index) => (
            <BetCard key={index} {...bet} />
          ))}
        </TabsContent>

        <TabsContent value="wins" className="space-y-4">
          {mockHistoricalBets
            .filter((b) => b.outcome === "win")
            .map((bet, index) => (
              <BetCard key={index} {...bet} />
            ))}
        </TabsContent>

        <TabsContent value="losses" className="space-y-4">
          {mockHistoricalBets
            .filter((b) => b.outcome === "loss")
            .map((bet, index) => (
              <BetCard key={index} {...bet} />
            ))}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default History;
