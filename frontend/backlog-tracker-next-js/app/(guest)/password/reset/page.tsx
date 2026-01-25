"use client";
import { apiFetch } from "@/lib/api";
import { useState } from "react";
import RandomColor from "@/components/RandomColor";

const PasswordReset = () => {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");
        setMessage("");
        try {
            await apiFetch("/authentication/password/reset/", {method: "POST", body: JSON.stringify({email}),});
            setMessage("Reset link sent! If not received, email may not exist.");
        }
        catch (error: any) {
            console.error("Error sending password reset:", error);
            setMessage("Reset link sent! If not received, email may not exist.");
        }
    };
    return (
        <div className = "min-h-screen flex items-center justify-center bg-main-compliment">
                <div className = "flex flex-col items-center gap-6">
                    <form onSubmit = {handleSubmit} className = "w-120 p-8 rounded-2xl shadow-2xl bg-ui">
                        <h1 className = "text-7xl text-white font-log-title mb-3">Password Reset</h1>
                        {message && <p className = "text-3xl text-white mb-3">{message}</p>}
                        {error && <p className = "text-3xl text-red-500">{error}</p>}
                        <input type = "email" value = {email} placeholder = "Email" onChange = {x => setEmail(x.target.value)} className = "btn w-103.5 mb-5 p-3" required />
                        <div className="flex justify-end mt-2">
                            <RandomColor element="bg"><button className = "btn">Send Reset Link</button></RandomColor>
                        </div>
                    </form>
                </div>
            </div>
    );
};

export default PasswordReset;