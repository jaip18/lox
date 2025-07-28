export default function Filter(){
    return(
        <div className="bg-green-500 m-10 flex items-center p-5">
            <ul className="flex list-none gap-10">
                <li className="inline-block bg-red-300">
                    league
                </li>
                <li className="inline-block bg-red-300"> 
                    bet type
                </li>
                <li className="inline-block bg-red-300">
                    sort by
                </li>
                <li className="inline-block bg-red-300">
                    interval
                </li>
            </ul>
        </div>
    );
}