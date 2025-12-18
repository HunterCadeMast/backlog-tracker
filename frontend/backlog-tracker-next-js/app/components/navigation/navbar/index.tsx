import React from "react"
import Link from "next/link"
import Logo from "./logo"
import Button from "./button"

const Navbar = () => {
    return (
        <>
            <div>
                <div>
                    <div>
                        <Logo />
                        <ul>
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
                        <Button />
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;