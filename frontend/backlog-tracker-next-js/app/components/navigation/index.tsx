"use client";
import { useState } from "react";
import Navbar from "./navbar";
import Sidebar from "./sidebar";

const NavigationPanel = () => {
    const [navigationState, setNavigationState] = useState(false);
    const navigationToggle = () => {
        setNavigationState(!navigationState);
    };
    return (
        <>
            <Sidebar navigationState = {navigationState} navigationToggle = {navigationToggle} />
            <Navbar navigationToggle = {navigationToggle} />
        </>
    );
};

export default NavigationPanel;