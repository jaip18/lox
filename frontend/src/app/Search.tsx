import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Search as SearchIcon, TrendingUp, TrendingDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const mockPlayers = [
  { name: "LeBron James", team: "LAL", position: "SF", ppg: 25.7, rpg: 7.3, apg: 7.3 },
  { name: "Stephen Curry", team: "GSW", position: "PG", ppg: 29.4, rpg: 6.1, apg: 6.3 },
  { name: "Jayson Tatum", team: "BOS", position: "SF", ppg: 27.1, rpg: 8.4, apg: 4.6 },
  { name: "Luka Doncic", team: "DAL", position: "PG", ppg: 33.9, rpg: 9.2, apg: 9.8 },
  { name: "Giannis Antetokounmpo", team: "MIL", position: "PF", ppg: 31.1, rpg: 11.8, apg: 5.7 },
];

const Search = () => {
  const [query, setQuery] = useState("");
  const [selectedPlayer, setSelectedPlayer] = useState<any>(null);

  const filteredPlayers = query
    ? mockPlayers.filter((p) =>
        p.name.toLowerCase().includes(query.toLowerCase())
      )
    : [];

  return (
    <div className="container py-8">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Player Search
          </h1>
          <p className="text-muted-foreground">
            Look up NBA players and view their stats
          </p>
        </div>

        <div className="mb-6 relative">
          <SearchIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search for a player..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-10 h-12 text-lg"
          />
        </div>

        {query && filteredPlayers.length > 0 && !selectedPlayer && (
          <Card className="mb-6 border-border bg-card p-2">
            <div className="space-y-1">
              {filteredPlayers.map((player) => (
                <button
                  key={player.name}
                  onClick={() => setSelectedPlayer(player)}
                  className="w-full rounded-lg p-3 text-left transition-colors hover:bg-secondary"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold">{player.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {player.team} • {player.position}
                      </p>
                    </div>
                    <Badge variant="outline">{player.ppg} PPG</Badge>
                  </div>
                </button>
              ))}
            </div>
          </Card>
        )}

        {selectedPlayer && (
          <Card className="border-border bg-gradient-card p-8">
            <div className="mb-6 flex items-start justify-between">
              <div>
                <h2 className="text-3xl font-bold">{selectedPlayer.name}</h2>
                <div className="mt-2 flex items-center gap-2">
                  <Badge variant="outline">{selectedPlayer.team}</Badge>
                  <Badge variant="secondary">{selectedPlayer.position}</Badge>
                </div>
              </div>
              <button
                onClick={() => setSelectedPlayer(null)}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Clear
              </button>
            </div>

            <div className="grid grid-cols-3 gap-6">
              <div className="rounded-lg border border-border bg-background p-4 text-center">
                <p className="text-sm text-muted-foreground">Points Per Game</p>
                <p className="mt-2 text-3xl font-bold text-primary">
                  {selectedPlayer.ppg}
                </p>
                <div className="mt-2 flex items-center justify-center gap-1 text-xs text-success">
                  <TrendingUp className="h-3 w-3" />
                  <span>+2.3 vs last season</span>
                </div>
              </div>

              <div className="rounded-lg border border-border bg-background p-4 text-center">
                <p className="text-sm text-muted-foreground">Rebounds Per Game</p>
                <p className="mt-2 text-3xl font-bold text-primary">
                  {selectedPlayer.rpg}
                </p>
                <div className="mt-2 flex items-center justify-center gap-1 text-xs text-muted-foreground">
                  <TrendingDown className="h-3 w-3" />
                  <span>-0.4 vs last season</span>
                </div>
              </div>

              <div className="rounded-lg border border-border bg-background p-4 text-center">
                <p className="text-sm text-muted-foreground">Assists Per Game</p>
                <p className="mt-2 text-3xl font-bold text-primary">
                  {selectedPlayer.apg}
                </p>
                <div className="mt-2 flex items-center justify-center gap-1 text-xs text-success">
                  <TrendingUp className="h-3 w-3" />
                  <span>+1.1 vs last season</span>
                </div>
              </div>
            </div>

            <div className="mt-6 rounded-lg border border-border bg-background p-4">
              <h3 className="mb-3 font-semibold">Recent Game Log</h3>
              <div className="space-y-2">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="text-muted-foreground">vs OPP</span>
                    <span className="font-medium">
                      {Math.floor(Math.random() * 15 + 15)} PTS, {Math.floor(Math.random() * 5 + 3)} REB, {Math.floor(Math.random() * 5 + 2)} AST
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Search;
