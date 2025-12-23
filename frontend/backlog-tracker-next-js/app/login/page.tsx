"use client";
import { useState } from "react";
import { loginAction } from "./action";
import Link from "next/link";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const handleSubmit = async (exception: React.FormEvent) => {
        exception.preventDefault();
        setError("");
        try {
            await loginAction(new FormData(exception.target as HTMLFormElement));
        }
        catch (caughtError: any) {
            setError(caughtError.message);
        }
    };
    return (
        <>
            <div className = "min-h-screen flex items-center justify-center bg-cream">
                <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-navbar">
                    <h1 className = "text-7xl text-gray-800 font-log-title mb-1">Login</h1>
                    {error && <p className = "text-3xl text-red-500 font-log-title mb-3">{error}</p>}
                    <input type = "email" name = "email" value = {email} onChange = {exception => setEmail(exception.target.value)} placeholder = "Email" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <input type = "password" name = "password" value = {password} onChange = {exception => setPassword(exception.target.value)} placeholder = "Password" className = "mb-3 p-3 text-3xl text-gray-800 font-log-title outline-3 outline-gray-800 rounded-2xl" required/>
                    <Link href= {"/password/reset"} className = "text-2xl text-gray-800 font-log-title">Forgot Password?</Link>
                    <button type = "submit" className = "ml-16.5 p-3 text-3xl text-white font-log-title rounded-2xl bg-gray-800">Login</button>
                </form>
            </div>
        </>
    );
};

export default Login;