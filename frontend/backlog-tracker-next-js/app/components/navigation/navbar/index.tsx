"use client";
import { useRouter } from "next/navigation";
import Link from "next/link"
import Image from "next/image";
import { useAuthentication } from "@/lib/authentication";
import SearchBar from "../../search/searchbar";
import RandomColor from "../../RandomColor";

type NavbarProps = {
    navigationToggle: () => void;
};

const Navbar = ({navigationToggle}: NavbarProps) => {
    const {user, logout} = useAuthentication();
    const router = useRouter();
    const handleLogout = () => {
        logout();
        router.push("/");
    };
    return (
        <>
            <div className = "navbar">
                <div className = "navbar-container p-2">
                    <div className = "flex items-center p-2">
                        <Link href = "/">
                            <Image src = {"/images/gaming-logjam-logo.svg"} alt = "gaming-logjam-logo" width = {62} height = {62} />
                        </Link>
                        <ul className = "hidden md:flex gap-x-7 pl-5 font-main-title text-white">
                            {user ? (
                                <>
                                    <li>
                                        <Link href = "/profile">
                                            <p><RandomColor>Profile</RandomColor></p>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link href = "/backlog">
                                            <p><RandomColor>Backlog</RandomColor></p>
                                        </Link>
                                    </li>
                                </>
                            ) : (<></>)}
                        </ul>
                    </div>
                    <div className = "flex items-center p-2">
                        <ul className = "hidden md:flex gap-x-7 pr-6.5">
                            {user ? (
                                <>
                                    <li>
                                        <RandomColor element = "bg"><button onClick = {handleLogout} className = "btn px-5">Logout</button></RandomColor>
                                    </li>
                                </>
                            ) : (
                                <>
                                    <li>
                                        <Link href = "/register">
                                            <RandomColor element = "bg"><button className = "btn px-5">Register</button></RandomColor>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link href = "/login">
                                            <RandomColor element = "bg"><button className = "btn px-5">Login</button></RandomColor>
                                        </Link>
                                    </li>
                                </>
                            )}
                        </ul>
                        <SearchBar />
                        <button className = "md:hidden justify-right p-2" onClick = {navigationToggle}>
                            <div className = "container">
                                <div className = "sideline"></div>
                                <div className = "sideline"></div>
                                <div className = "sideline"></div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;