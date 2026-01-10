"use client";
import { apiFetch } from "@/lib/api";
import { useState } from "react";

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
        catch {
            setMessage("Reset link sent! If not received, email may not exist.");
        }
    };
    return (
        <div className = "min-h-screen flex items-center justify-center bg-cream">
            <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-navbar">
                <h1 className = "text-6xl font-log-title mb-4">Password Reset</h1>
                {message && <p className = "text-3xl text-gray-800">{message}</p>}
                {error && <p className = "text-3xl text-red-500">{error}</p>}
                <input type = "email" value = {email} placeholder = "Email" onChange = {x => setEmail(x.target.value)} className = "mb-3 p-3 text-3xl rounded-2xl" required />
                <button className = "p-3 text-3xl text-white bg-gray-800 rounded-2xl">Send Reset Link</button>
            </form>
        </div>
    );
};

export default PasswordReset;