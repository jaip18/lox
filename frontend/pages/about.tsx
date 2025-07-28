import Navbar from "@/components/Navbar";

export default function About() {
    return(
        <div>
            <Navbar></Navbar>

            <div className="bg-orange-400 mx-auto my-20 rounded-4xl w-fit">
                <h1 className="p-10 font-bold text-2xl">
                    DISCLOSER: I DO NOT SPORTS GAMBLE NOR DO I ENCOURAGE IT!!!
                </h1>
            </div>

            <div className="bg-gray-400 flex mx-20 rounded-2xl">
                <p className="text-2xl p-5">
                    Using insights and the philosophy of my friends who do dable in 
                    the "infinite money glitch" (My Gambling Friends, 2025), I was able 
                    to create a betting engine which can simulate and visualize their
                    thought-processes. Although I do not partake myself, as a Computer 
                    Science student I figured this would be a good opportunity to learn about
                    and develop my own full-stack application.
                    <br></br>
                    <br></br>
                    Lox is a homophone for locks, cause I'm only providing you with locks on
                    all of your parlays
                    <br></br>
                    <a className="text-blue-500">github icon</a>
                    <a className="text-blue-800"> vercel</a>
                </p>
                
            </div>
        </div>
    );
}