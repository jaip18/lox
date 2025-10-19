import { BetCard } from "@/components/BetCard";
import { FilterPanel } from "@/components/FilterPanel";
import { ScoresPanel } from "@/components/ScoresPanel";

const mockBets = [
  {
    playerName: "LeBron James",
    team: "LAL",
    opponent: "GSW",
    betType: "Over",
    line: 25.5,
    confidence: 91,
    gameDate: "Today, 7:30 PM",
  },
  {
    playerName: "Stephen Curry",
    team: "GSW",
    opponent: "LAL",
    betType: "Over",
    line: 4.5,
    confidence: 87,
    gameDate: "Today, 7:30 PM",
  },
  {
    playerName: "Jayson Tatum",
    team: "BOS",
    opponent: "MIA",
    betType: "Over",
    line: 27.5,
    confidence: 84,
    gameDate: "Today, 8:00 PM",
  },
  {
    playerName: "Luka Doncic",
    team: "DAL",
    opponent: "PHX",
    betType: "Over",
    line: 8.5,
    confidence: 79,
    gameDate: "Today, 9:00 PM",
  },
];

const Dashboard = () => {
  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
          Today's Top Bets
        </h1>
        <p className="text-muted-foreground">
          AI-powered prop bet recommendations with confidence scores
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <aside className="lg:col-span-3">
          <FilterPanel />
        </aside>

        <main className="lg:col-span-6">
          <div className="space-y-4">
            {mockBets.map((bet, index) => (
              <BetCard key={index} {...bet} />
            ))}
          </div>
        </main>

        <aside className="lg:col-span-3">
          <ScoresPanel />
        </aside>
      </div>
    </div>
  );
};

export default Dashboard;
