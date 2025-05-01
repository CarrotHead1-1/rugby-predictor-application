import Image from "next/image"
import logo from '@/public/appLogo.png'
import Link from "next/link"

const Navbar = () => {
    return (
        <nav className='fixed w-full h-24 shadow-xl bg-white'>
            <div className='flex justify-between items-center h-full w-full px-4 py-2'>
                <Link href='/'>
                    <Image src={logo} alt="logo" width="64" height="64" className="border-2 shadow-xl bg-black rounded-2xl"></Image>
                </Link>
                <div>
                    <ul className="hidden sm:flex">
                        <Link href="/elo">
                            <li className="ml-10 uppercase hover:border-b text-xl"> Elo History </li>
                        </Link>
                        <Link href="/h2h">
                            <li className="ml-10 uppercase hover:border-b text-xl"> H2H Results </li>
                        </Link>

                    </ul>
                </div>
            </div>
        </nav>
    )
}

export default Navbar