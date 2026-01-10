"use client";
import { apiFetch } from "@/lib/api";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";

const PasswordResetConfirmPassword = () => {
    const router = useRouter();
    const {id, token} = useParams();
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");
        if (newPassword !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }
        try {
            await apiFetch(`/authentication/password/reset/${id}/${token}/`, {method: "POST", body: JSON.stringify({new_password: newPassword, new_password_confirm: confirmPassword}),});
            setMessage("Password reset!");
            setTimeout(() => router.push("/login"), 2000);
        }
        catch (error: any) {
            setError(error.message || "Password reset failed!");
        }
    };
    return (
        <div className = "min-h-screen flex items-center justify-center bg-cream">
            <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-navbar">
                <h1 className = "text-6xl font-log-title mb-4">New Password</h1>
                {message && <p className = "text-3xl text-gray-800">{message}</p>}
                {error && <p className = "text-3xl text-red-500">{error}</p>}
                <input type = "password" value = {newPassword} placeholder = "New Password" onChange = {x => setNewPassword(x.target.value)} className = "mb-3 p-3 text-3xl rounded-2xl" required />
                <input type = "password" value = {confirmPassword} placeholder = "Confirm New Password" onChange = {x => setConfirmPassword(x.target.value)} className = "mb-3 p-3 text-3xl rounded-2xl" required />
                <button className = "p-3 text-3xl text-white bg-gray-800 rounded-2xl">Reset Password</button>
            </form>
        </div>
    );
};

export default PasswordResetConfirmPassword;