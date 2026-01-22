"use client";
import {useEffect} from "react";
import {useRouter} from "next/navigation";
import {useAuthentication} from "@/src/lib/authentication";

const UserGuest = ({children}: {children: React.ReactNode}) => {
    const {user, loading} = useAuthentication();
    const router = useRouter();
    useEffect(() => {
        if (!loading && user) {
            router.replace("/");
        }
    }, [user, loading, router]);
    if (loading) return null;
    return <>{children}</>;
};

export default UserGuest;