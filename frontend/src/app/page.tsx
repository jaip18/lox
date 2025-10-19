"use client"; // Add this line to make it a Client Component

import { useState, useEffect } from "react";
import { Navigation } from "@/components/Navigation";
import { ScoresPanel } from "@/components/ScoresPanel";
import { FilterPanel } from "@/components/FilterPanel";
import { BetCard } from "@/components/BetCard";
import { Info, SlidersHorizontal } from "lucide-react";

// This is your main Homepage component, which corresponds to the `/` route.
export default function HomePage() {
  // 1. Updated Mock Data to match the actual BetCardProps
  const allBets = [
    {
      id: 1,
      playerName: "LeBron James",
      team: "LAL",
      opponent: "GSW",
      betType: "Points",
      line: 28.5,
      confidence: 82,
      gameDate: "Oct 18, 2025",
      outcome: null,
    },
    {
      id: 2,
      playerName: "Stephen Curry",
      team: "GSW",
      opponent: "LAL",
      betType: "3-Pointers",
      line: 4.5,
      confidence: 75,
      gameDate: "Oct 18, 2025",
      outcome: "win",
    },
    {
      id: 3,
      playerName: "Nikola Jokic",
      team: "DEN",
      opponent: "PHX",
      betType: "Rebounds",
      line: 12.5,
      confidence: 65,
      gameDate: "Oct 19, 2025",
      outcome: "loss",
    },
    {
      id: 4,
      playerName: "Kevin Durant",
      team: "PHX",
      opponent: "DEN",
      betType: "Points",
      line: 29.5,
      confidence: 58,
      gameDate: "Oct 19, 2025",
      outcome: null,
    },
  ];

  // 2. State management for filters and the bets that are displayed
  const [filters, setFilters] = useState({
    confidence: 70,
    betType: 'all',
  });
  const [filteredBets, setFilteredBets] = useState(allBets);

  // 3. This effect runs whenever the 'filters' state changes
  useEffect(() => {
    let bets = allBets;

    // Filter by confidence score
    bets = bets.filter(bet => bet.confidence >= filters.confidence);
    
    // Filter by bet type
    if (filters.betType !== 'all') {
      bets = bets.filter(bet => bet.betType.toLowerCase().includes(filters.betType));
    }

    setFilteredBets(bets);
  }, [filters]);


  // 4. Handler to update filters from the FilterPanel component
  const handleFilterChange = (newFilters: any) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };


  return (
    <div className="flex min-h-screen w-full flex-col bg-muted/40">
      <Navigation />
      <main className="flex-1 p-4 sm:p-6 lg:p-8">
        <div className="container mx-auto grid grid-cols-1 gap-6 lg:grid-cols-12">
          
          <aside className="lg:col-span-3">
            <ScoresPanel />
          </aside>

          <div className="lg:col-span-6">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold">Player Props</h1>
               <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <SlidersHorizontal className="h-4 w-4" />
                <span>{filteredBets.length} Results</span>
               </div>
            </div>
            
            {/* 5. Map over the *filtered* bets state */}
            <div className="space-y-4">
              {filteredBets.length > 0 ? (
                filteredBets.map((bet) => (
                  <BetCard
                    key={bet.id}
                    playerName={bet.playerName}
                    team={bet.team}
                    opponent={bet.opponent}
                    betType={bet.betType}
                    line={bet.line}
                    confidence={bet.confidence}
                    gameDate={bet.gameDate}
                    outcome={bet.outcome}
                  />
                ))
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <p>No bets match the current filters.</p>
                </div>
              )}
            </div>

            <div className="mt-6 flex items-center gap-3 rounded-lg border bg-card p-4 text-sm text-muted-foreground">
              <Info className="h-5 w-5" />
              <p>Odds are subject to change. Always check with your provider.</p>
            </div>
          </div>

          <aside className="lg:col-span-3">
            {/* 6. Pass the handler function to the FilterPanel */}
            <FilterPanel onFiltersChange={handleFilterChange} />
          </aside>

        </div>
      </main>
    </div>
  );
}

