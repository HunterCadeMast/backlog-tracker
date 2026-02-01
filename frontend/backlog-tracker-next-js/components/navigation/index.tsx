"use client";
import { useState } from "react";
import Navbar from "./navbar";
import Sidebar from "./sidebar";
import { useAuthentication } from "@/lib/authentication";

const NavigationPanel = () => {
    const [navigationState, setNavigationState] = useState(false);
    const { user, logout } = useAuthentication();
    const navigationToggle = () => {
        setNavigationState(!navigationState);
    };
    return (
        <>
            <Sidebar navigationState = {navigationState} navigationToggle = {navigationToggle} user = {user} logout = {logout} />
            <Navbar navigationToggle = {navigationToggle} />
        </>
    );
};

export default NavigationPanel;