"use client";
import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthentication } from "@/src/lib/authentication";

const OAuthCallback = () => {
    const router = useRouter();
    const {refreshUser} = useAuthentication();
    const params = useSearchParams();
    useEffect(() => {
        const access = params.get("access");
        const refresh = params.get("refresh");
        if (!access || !refresh) {
            router.push("/login");
            return;
        }
        localStorage.setItem("access", access);
        localStorage.setItem("refresh", refresh);
        refreshUser().then(() => {router.push("/");});
    }, [params, router]);
    return <p>Signing in…</p>;
};

export default OAuthCallback;