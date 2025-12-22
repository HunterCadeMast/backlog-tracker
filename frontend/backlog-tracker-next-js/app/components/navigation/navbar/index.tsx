import React from "react"
import Link from "next/link"
import Logjam from "./logjam-logo"

type NavbarProps = {
    navigationToggle: () => void;
};

const Navbar = ({navigationToggle}: NavbarProps) => {
    return (
        <>
            <div className = "sticky top-0 bg-navbar">
                <div className = "container flex items-center justify-between max-w-screen mx-auto px-4">
                    <div className = "flex items-center p-2">
                        <Logjam />
                        <ul className = "hidden md:flex gap-x-7 pl-5 font-main-title  text-gray-800">
                            <li>
                                <Link href = "/profile">
                                    <p>Profile</p>
                                </Link>
                            </li>
                            <li>
                                <Link href = "/backlog">
                                    <p>Backlog</p>
                                </Link>
                            </li>
                        </ul>
                    </div>
                    <div className = "flex items-center p-2">
                        <ul className = "hidden md:flex gap-x-7 pr-5 font-main-title font-bold text-cream">
                            <li>
                                <Link href = "/login">
                                    <button className = "h-10 rounded-lg bg-button outline-4 outline-button-border px-5">Login</button>
                                </Link>
                            </li>
                        </ul>
                        <button className = "md:hidden justify-right p-2" onClick = {navigationToggle}>
                            <div className = "container">
                                <div className = "w-10 h-1 bg-gray-800 m-1.5"></div>
                                <div className = "w-10 h-1 bg-gray-800 m-1.5"></div>
                                <div className = "w-10 h-1 bg-gray-800 m-1.5"></div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;