"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { useParams } from "next/navigation";

const EmailVerification = () => {
    const {id, token} = useParams();
    const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
    const [message, setMessage] = useState("");
    useEffect(() => {
        apiFetch(`/authentication/email/verifiation/${id}/${token}/`)
            .then(response => {
                setMessage(response.message);
                setStatus("success");
            })
            .catch(error => {
                setMessage(error.message || "Verification failed!");
                setStatus("error");
            });
    }, [id, token]);
    return (
        <div className = "min-h-screen flex items-center justify-center bg-main-compliment">
            <div className = "w-90 p-8 rounded-2xl shadow-2xl bg-ui">
                <h1 className = "text-6xl font-log-title mb-4">Email Verification</h1>
                <p className = {`text-3xl font-log-title ${status === "error" ? "text-red-500" : "text-gray-800"}`}>{status === "loading" ? "Verifying..." : message}</p>
            </div>
        </div>
    );
};

export default EmailVerification;