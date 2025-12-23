"use client";
import { useEffect } from "react";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";

const Logout = () => {
    const router = useRouter();
    useEffect(() => {
        async function logout() {
            await apiFetch("/accounts/logout/", {method: "POST"});
            router.push("/login");
        }
        logout();
    }, [router]);
    return (
        <>
            <div>
                <h1>Logging Out</h1>
            </div>
        </>
    );
};

export default Logout;