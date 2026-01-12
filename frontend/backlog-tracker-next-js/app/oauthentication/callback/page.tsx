"use client";
import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function OAuthCallback() {
    const router = useRouter();
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
        router.push("/");
    }, [params, router]);
    return <p>Signing in…</p>;
}
