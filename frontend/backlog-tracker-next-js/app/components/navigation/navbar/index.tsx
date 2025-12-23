"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { userFetch } from "@/lib/authentication";
import Link from "next/link"
import Logjam from "./logjam-logo"

type NavbarProps = {
    navigationToggle: () => void;
};

const Navbar = ({navigationToggle}: NavbarProps) => {
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    useEffect(() => {
        async function user() {
            const account = await userFetch();
            setUser(account);
            setLoading(false);
        }
        user();
    }, []);
    const handleLogout = async () => {
        await apiFetch("/accounts/logout/", {method: "POST"});
        setUser(null);
        router.push("login");
    };
    if (loading) {
        return null;
    }
    else {
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
                                {user ? (
                                    <>
                                        <li>
                                            <Link href = "/logout">
                                                <button onClick = {handleLogout} className = "h-10 rounded-lg bg-button outline-4 outline-button-border px-5">Logout</button>
                                            </Link>
                                        </li>
                                    </>
                                ) : (
                                    <>
                                        <li>
                                            <Link href = "/register">
                                                <button className = "h-10 rounded-lg bg-button outline-4 outline-button-border px-5">Register</button>
                                            </Link>
                                        </li>
                                        <li>
                                            <Link href = "/login">
                                                <button className = "h-10 rounded-lg bg-button outline-4 outline-button-border px-5">Login</button>
                                            </Link>
                                        </li>
                                    </>
                                )}
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
    }
};

export default Navbar;