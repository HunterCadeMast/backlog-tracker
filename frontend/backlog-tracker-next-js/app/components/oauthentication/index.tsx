const OAuthenticationButtons = ({provider}: {provider: "google" | "github"}) => {
    return (
        <a href = {`${process.env.NEXT_PUBLIC_BACKEND_URL}/accounts/${provider}/login/?process=login`} className = "p-3 text-3xl text-white bg-gray-800 rounded-2xl text-center">
            Continue with {provider === "google" ? "Google" : "GitHub"}
        </a>
    );
};

export default OAuthenticationButtons;