import Image from "next/image"
import logo from '@/public/appLogo.png'
import Link from "next/link"

const Navbar = () => {
    return (
        <nav className='fixed top-0 w-full h-20 shadow-md bg-white z-50'>
            <div className='flex justify-between items-center h-full w-full px-4 md:px-8'>
                <Link href='/' className="flex justify-between items-center h-full w-full pz-4 md:px-8">
                    <Image src={logo} alt="logo" width="64" height="64" className="border-2 shadow-xl bg-black rounded-2xl"></Image>
                    <span className="text-xl font-bold sm:inline"> Rugby Prediction App </span>
                </Link>


                <ul className="hidden sm:flex space-x-6 text-lg font-medium">

                    <li className="hover"> <Link href="/"> Home</Link></li>
                    <li className="hover"> <Link href="/elo"> ELo Hisotry </Link> </li>


                </ul>
            </div>

        </nav>
    )
}

export default Navbar