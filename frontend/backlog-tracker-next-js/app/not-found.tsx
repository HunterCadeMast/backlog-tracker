const NotFound = () => {
    return (
        <div className = "base-background flex flex-col items-center justify-center text-center">
            <h2 className = "text-6xl font-main-title">404: Page Not Found</h2>
            <p className = "mt-5">Could not find requested resource.</p>
        </div>
    );
};

export default NotFound;