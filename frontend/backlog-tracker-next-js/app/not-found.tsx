import React from "react";

const NotFound = () => {
    return (
        <div className = "min-h-screen flex flex-col items-center justify-center">
            <h2 className = "text-6xl font-main-title">404: Page Not Found</h2>
            <p className = "mt-5">Could not find requested resource.</p>
        </div>
    );
};

export default NotFound;