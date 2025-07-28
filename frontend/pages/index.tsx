import Navbar from "@/components/Navbar";
import Filter from "@/components/Filter";
import Tableau from "@/components/BetTableau";
import Scoreboard from "@/components/Scoreboard";

export default function Home() {
  return (
    <div>
      <Navbar></Navbar>
      <Filter></Filter>
      <div className="flex">
        <Tableau></Tableau>
        <Scoreboard></Scoreboard>
      </div>
    </div>
  );
}
