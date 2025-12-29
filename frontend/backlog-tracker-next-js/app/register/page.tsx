"use client";
import { useState } from "react";
import { registerAction } from "./action";

const Register = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");
    const handleSubmit = async (exception: React.FormEvent) => {
        exception.preventDefault();
        setError("");
        try {
            await registerAction(new FormData(exception.target as HTMLFormElement));
        }
        catch (caughtError: any) {
            setError(caughtError?.password1?.[0] || caughtError?.password2?.[0] || caughtError?.email?.[0] || caughtError?.username?.[0] || caughtError?.detail?.[0] || "Registration failed!");
        }
    };
    return (
        <>
            <div className = "min-h-screen flex items-center justify-center bg-cream">
                <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-navbar">
                    <h1 className = "text-7xl text-gray-800 font-log-title mb-1">Register</h1>
                    {error && <p className = "text-3xl text-red-500 font-log-title mb-3">{error}</p>}
                    <input type = "username" name = "username" value = {username} onChange = {exception => setUsername(exception.target.value)} placeholder = "Username" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <input type = "email" name = "email" value = {email} onChange = {exception => setEmail(exception.target.value)} placeholder = "Email" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <input type = "password" name = "password1" value = {password1} onChange = {exception => setPassword1(exception.target.value)} placeholder = "Password" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <input type = "password" name = "password2" value = {password2} onChange = {exception => setPassword2(exception.target.value)} placeholder = "Verify Password" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <button type = "submit" className = "ml-45 p-3 text-3xl text-white font-log-title rounded-2xl bg-gray-800">Register</button>
                </form>
            </div>
        </>
    );
};

export default Register;