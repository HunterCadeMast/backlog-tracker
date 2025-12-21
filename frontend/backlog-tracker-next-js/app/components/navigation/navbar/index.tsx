import React from "react"
import Link from "next/link"
import Logjam from "./logjam-logo"
import Button from "./button"

type NavbarProps = {
    navigationToggle: () => void;
};

const Navbar = ({navigationToggle}: NavbarProps) => {
    return (
        <>
            <div className = "sticky top-0 flex h-20 bg-navbar">
                <div className = "container flex items-center justify-between max-w-7xl mx-auto px-4">
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
                        <ul className = "hidden md:flex gap-x-7 pr-5 font-main-title  text-gray-800">
                            <li>
                                <Link href = "/signin">
                                    <p>Sign In</p>
                                </Link>
                            </li>
                        </ul>
                        <button onClick = {navigationToggle}>
                            <Button />
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;