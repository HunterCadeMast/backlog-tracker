import RandomColor from "../RandomColor";

const OAuthenticationButtons = ({provider}: {provider: "google" | "github"}) => {
    return (
        <RandomColor element = "bg">
            <a href = {`${process.env.NEXT_PUBLIC_BACKEND_URL}/accounts/${provider}/login/?process=login`} className = "bg-ui text-3xl btn">
                Continue with {provider === "google" ? "Google" : "GitHub"}
            </a>
        </RandomColor>
    );
};

export default OAuthenticationButtons;