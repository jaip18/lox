import BetTab from "./BetTab";

export default function Tableau(){
    return(
        <div className="w-3/5 h-fit bg-green-700 rounded-4xl m-10 p-5">
            <BetTab></BetTab>
            <BetTab></BetTab>
            <BetTab></BetTab>
            <BetTab></BetTab>
            <BetTab></BetTab>
        </div>
    );
}