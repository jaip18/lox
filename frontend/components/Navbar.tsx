import Link from "next/link";

export default function Navbar(){
    return (
        <div className="w-full top-0 flex justify-between sticky m-auto bg-amber-300">
            <div className="flex justify-center items-center m-10 bg-blue-600">
                <Link href='/'>
                    lox
                </Link>
            </div>

            <nav className="flex justify-center items-center p-10 bg-red-500 mr-10">
                <ul className="flex list-none gap-20">
                    <li className="inline-block">
                        <Link href="/search">
                            search
                        </Link>
                    </li>

                    <li className="inline-block">
                        <Link href="/loxhistory">
                            fg%
                        </Link>
                    </li>

                    <li className="inline-block">
                        <Link href="/scores">
                            scores
                        </Link>
                    </li>

                    <li className="inline-block">
                        <Link href="/about">
                            about
                        </Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
}