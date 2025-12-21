import Image from "next/image";
import Link from "next/link";

const Logo = () => {
    return (
        <>
            <Link href = "/">
                <Image src = {"/images/gaming-logjam-logo.svg"} alt = "gaming-logjam-logo" width = {62} height = {62} />
            </Link>
        </>
    );
};

export default Logo;