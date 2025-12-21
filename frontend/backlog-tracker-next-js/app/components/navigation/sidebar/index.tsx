import React from "react";

type SidebarProps = {
    navigationState: boolean;
    navigationToggle: () => void;
};

const Sidebar = ({navigationState, navigationToggle}: SidebarProps) => {
    return (
        <div>
            Sidebar
        </div>
    );
};

export default Sidebar;