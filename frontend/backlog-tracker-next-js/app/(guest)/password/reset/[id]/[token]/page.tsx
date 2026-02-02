"use client";
import { apiFetch } from "@/lib/api";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import RandomColor from "@/components/RandomColor";

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
        const key = `password_reset_${id}_${token}`;
        if (localStorage.getItem(key)) {
            setError("This password reset link has already been used!");
            return;
        }
        try {
            await apiFetch(`/authentication/password/reset/${id}/${token}/`, {
                method: "POST",
                body: JSON.stringify({
                    new_password: newPassword,
                    new_password_confirm: confirmPassword,
                }),
            });
            localStorage.setItem(key, "true");
            setMessage("Password reset! Please login again...");
            setTimeout(() => router.replace("/login"), 2000);
        }
        catch (error: any) {
            setError(error.message || "Password reset failed!");
        }
    };
    return (
        <div className = "h-full flex items-center justify-center bg-main-compliment">
            <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-ui">
                <h1 className = "text-5xl sm:text-7xl font-log-title mb-4">Reset Password</h1>
                {message && <p className = "text-3xl text-white mb-5">{message}</p>}
                {error && <p className = "text-3xl text-red-500 mb-5">{error}</p>}
                <input type = "password" value = {newPassword} placeholder = "New Password" onChange = {x => setNewPassword(x.target.value)} className = "btn w-full mb-5 p-3" required />
                <input type = "password" value = {confirmPassword} placeholder = "Confirm Password" onChange = {x => setConfirmPassword(x.target.value)} className = "btn w-full mb-5 p-3" required />
                <div className="flex justify-end mt-4">
                    <RandomColor element="bg"><button type="submit" className="btn mr-2">Reset Password</button></RandomColor>
                </div>
            </form>
        </div>
    );
};

export default PasswordResetConfirmPassword;