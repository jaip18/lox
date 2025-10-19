import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Trophy, Clock } from "lucide-react";

interface Game {
  id: string;
  homeTeam: string;
  awayTeam: string;
  homeScore: number;
  awayScore: number;
  status: string;
  topPerformers?: { name: string; stats: string }[];
}

const mockGames: Game[] = [
  {
    id: "1",
    homeTeam: "Los Angeles Lakers",
    awayTeam: "Golden State Warriors",
    homeScore: 112,
    awayScore: 108,
    status: "Final",
    topPerformers: [
      { name: "LeBron James", stats: "28 PTS, 7 REB, 8 AST" },
      { name: "Stephen Curry", stats: "31 PTS, 5 REB, 6 AST" },
    ],
  },
  {
    id: "2",
    homeTeam: "Boston Celtics",
    awayTeam: "Miami Heat",
    homeScore: 98,
    awayScore: 95,
    status: "Q4 2:35",
    topPerformers: [
      { name: "Jayson Tatum", stats: "24 PTS, 9 REB, 5 AST" },
      { name: "Jimmy Butler", stats: "22 PTS, 6 REB, 4 AST" },
    ],
  },
  {
    id: "3",
    homeTeam: "Phoenix Suns",
    awayTeam: "Dallas Mavericks",
    homeScore: 89,
    awayScore: 91,
    status: "Q3 8:12",
    topPerformers: [
      { name: "Kevin Durant", stats: "19 PTS, 5 REB, 3 AST" },
      { name: "Luka Doncic", stats: "26 PTS, 8 REB, 7 AST" },
    ],
  },
  {
    id: "4",
    homeTeam: "Milwaukee Bucks",
    awayTeam: "Denver Nuggets",
    homeScore: 0,
    awayScore: 0,
    status: "7:30 PM ET",
  },
];

const Scores = () => {
  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
          NBA Scores
        </h1>
        <p className="text-muted-foreground">Live and recent game scores</p>
      </div>

      <Tabs defaultValue="today" className="space-y-6">
        <TabsList>
          <TabsTrigger value="today">Today</TabsTrigger>
          <TabsTrigger value="yesterday">Yesterday</TabsTrigger>
          <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
        </TabsList>

        <TabsContent value="today" className="space-y-4">
          {mockGames.map((game) => (
            <Card key={game.id} className="border-border bg-gradient-card p-6">
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Trophy className="h-5 w-5 text-primary" />
                  <span className="text-sm font-medium text-muted-foreground">
                    {game.status.includes("PM") ? "Upcoming" : game.status}
                  </span>
                </div>
                {game.status === "Final" ? (
                  <Badge variant="outline">Final</Badge>
                ) : game.status.includes("PM") ? (
                  <Badge variant="secondary" className="gap-1">
                    <Clock className="h-3 w-3" />
                    {game.status}
                  </Badge>
                ) : (
                  <Badge variant="default" className="animate-pulse">
                    Live
                  </Badge>
                )}
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between rounded-lg bg-background p-4">
                  <span className="text-lg font-semibold">{game.awayTeam}</span>
                  <span className="text-3xl font-bold">
                    {game.awayScore || "-"}
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-lg bg-background p-4">
                  <span className="text-lg font-semibold">{game.homeTeam}</span>
                  <span className="text-3xl font-bold">
                    {game.homeScore || "-"}
                  </span>
                </div>
              </div>

              {game.topPerformers && (
                <div className="mt-4 border-t border-border pt-4">
                  <p className="mb-2 text-sm font-medium text-muted-foreground">
                    Top Performers
                  </p>
                  <div className="space-y-2">
                    {game.topPerformers.map((performer, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between text-sm"
                      >
                        <span className="font-medium">{performer.name}</span>
                        <span className="text-muted-foreground">
                          {performer.stats}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="yesterday">
          <p className="text-center text-muted-foreground">No games yesterday</p>
        </TabsContent>

        <TabsContent value="upcoming">
          <p className="text-center text-muted-foreground">No upcoming games</p>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Scores;
