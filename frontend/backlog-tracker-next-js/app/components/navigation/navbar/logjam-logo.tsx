import Image from "next/image";

const Logo = () => {
    return (
        <>
            <Image src = {"/images/gaming-logjam-logo.svg"} alt = "gaming-logjam-logo" width = {62} height = {62} />
        </>
    );
};

export default Logo;