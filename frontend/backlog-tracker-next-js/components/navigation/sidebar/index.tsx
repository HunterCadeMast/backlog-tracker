import Link from "next/link";

type SidebarProps = {
    navigationState: boolean;
    navigationToggle: () => void;
    user: any;
    logout: () => void;
};

const Sidebar = ({navigationState, navigationToggle, user, logout}: SidebarProps) => {
    return (
        <>
            <div className = {`fixed w-full h-full overflow-hidden justify-center grid pt-30 left-0 z-10 bg-main-compliment ${navigationState ? "opacity-100 top-0 pointer-events-auto" : "opacity-0 -top-full pointer-events-none"}`}>
                <button className = "absolute right-0 p-8" onClick = {navigationToggle}>
                    <div className = "container">
                        <div className = {`w-10 h-1 bg-white m-1.5 transition-all duration-500 ${navigationState ? `translate-y-2.5 -rotate-45` : ''}`}></div>
                        <div className = {`w-10 h-1 bg-white m-1.5 transition-all duration-500 ${navigationState ? `opacity-0` : ''}`}></div>
                        <div className = {`w-10 h-1 bg-white m-1.5 transition-all duration-500 ${navigationState ? `-translate-y-2.5 rotate-45` : ''}`}></div>
                    </div>
                </button>
                <ul className = "flex flex-col items-center justify-center gap-6 font-main-title text-white text-2xl">
                    {user ? (
                        <>
                            <li>
                                <Link href = "/profile" onClick = {navigationToggle} className = "btn">Profile</Link>
                            </li>
                            <li>
                                <Link href = "/backlog" onClick = {navigationToggle} className = "btn">Backlog</Link>
                            </li>
                            <li>
                                <button onClick={() => {logout(); navigationToggle();}} className = "btn mt-2">Logout</button>
                            </li>
                        </>
                    ) : (
                        <>
                            <li>
                                <Link href = "/register" onClick = {navigationToggle} className = "btn">Register</Link>
                            </li>
                            <li>
                                <Link href = "/login" onClick = {navigationToggle} className = "btn">Login</Link>
                            </li>
                        </>
                    )}
                </ul>
            </div>
        </>
    );
};

export default Sidebar;