"use client";
import {useEffect} from "react";
import {useRouter, usePathname} from "next/navigation";
import {useAuthentication} from "@/lib/authentication";

const UserAuthentication = ({children}: {children: React.ReactNode}) => {
    const {user, loading} = useAuthentication();
    const router = useRouter();
    const pathname = usePathname();
    useEffect(() => {
        if (!loading && !user) {
            router.replace(`/login?next=${pathname}`);
        }
    }, [user, loading, router, pathname]);
    if (loading || !user) return null;
    return <>{children}</>;
};

export default UserAuthentication;