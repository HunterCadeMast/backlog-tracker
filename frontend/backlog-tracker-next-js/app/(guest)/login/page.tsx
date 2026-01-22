"use client";
import { useState } from "react";
import { loginAction } from "./action";
import { useRouter } from "next/navigation";
import { useAuthentication } from "@/lib/authentication";
import Link from "next/link";
import OAuthenticationButtons from "@/components/oauthentication";
import RandomColor from "@/components/RandomColor";

const Login = () => {
    const router = useRouter();
    const {refreshUser} = useAuthentication();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<Record<string, string[]>>({});
    const [success, setSuccess] = useState("");
    const handleSubmit = async (exception: React.FormEvent<HTMLFormElement>) => {
        exception.preventDefault();
        setError({});
        setSuccess("")
        try {
            await loginAction(new FormData(exception.currentTarget));
            setSuccess("Successfully logged in!");
            await refreshUser();
            router.push("/");
        }
        catch (caughtError: any) {
            setError(caughtError);
        }
    };
    return (
        <>
            <div className = "min-h-screen flex items-center justify-center bg-main-compliment">
                <div className = "flex flex-col items-center gap-6">
                    <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-ui">
                        <h1 className = "text-7xl text-white font-log-title mb-3">Login</h1>
                        <div className="flex justify-left mb-5">
                            <Link href= {"/password/reset"} className = "text-2xl text-white font-log-title">Forgot Password?</Link>
                        </div>
                        {error.non_field_errors && <p className = "text-3xl text-red-500 font-log-title mb-5">{error.non_field_errors[0]}</p>}
                        {success && <p className = "text-3xl text-white font-log-title mb-5">{success}</p>}
                        <input type = "email" name = "email" value = {email} onChange = {exception => setEmail(exception.target.value)} placeholder = "Email" className = "input-element" required/>
                        <input type = "password" name = "password" value = {password} onChange = {exception => setPassword(exception.target.value)} placeholder = "Password" className = "input-element" required/>
                        <div className="flex justify-end mt-2">
                            <RandomColor element="bg"><button type="submit" className="text-2xl btn mr-2">Submit</button></RandomColor>
                        </div>
                    </form>
                    <div className = "flex gap-4">
                        <OAuthenticationButtons provider = "google" />
                        <OAuthenticationButtons provider = "github" />
                    </div>
                </div>
            </div>
        </>
    );
};

export default Login;