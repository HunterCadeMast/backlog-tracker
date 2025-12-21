import {useState} from "react";
import Link from "next/link";

type SidebarProps = {
    navigationState: boolean;
    navigationToggle: () => void;
};

const Sidebar = ({navigationState, navigationToggle}: SidebarProps) => {
    return (
        <>
            <div className = {`fixed w-full h-full overflow-hidden justify-center grid pt-30 left-0 z-10 bg-cream ${navigationState ? "opacity-100 top-0 pointer-events-auto" : "opacity-0 -top-full pointer-events-none"}`}>
                <button className = "absolute right-2.5 p-5.5" onClick = {navigationToggle}>
                    <div className = "container">
                        <div className = {`w-10 h-1 bg-gray-800 m-1.5 transition-all duration-500 ${navigationState ? `translate-y-2.5 -rotate-45` : ''}`}></div>
                        <div className = {`w-10 h-1 bg-gray-800 m-1.5 transition-all duration-500 ${navigationState ? `opacity-0` : ''}`}></div>
                        <div className = {`w-10 h-1 bg-gray-800 m-1.5 transition-all duration-500 ${navigationState ? `-translate-y-2.5 rotate-45` : ''}`}></div>
                    </div>
                </button>
                <ul className = "gap-x-7 pl-5 font-main-title  text-gray-800">
                    <li>
                        <Link href = "/profile" onClick = {navigationToggle}>
                            <p>Profile</p>
                        </Link>
                    </li>
                    <li>
                        <Link href = "/backlog" onClick = {navigationToggle}>
                            <p>Backlog</p>
                        </Link>
                    </li>
                </ul>
            </div>
        </>
    );
};

export default Sidebar;