"use client";
import { useState } from "react";
import { registerAction } from "./action";
import OAuthenticationButtons from "../components/oauthentication/";
import RandomColor from "../components/RandomColor";

const Register = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");
    const [acceptedPrivacy, setAcceptedPrivacy] = useState(false);
    const [acceptedTerms, setAcceptedTerms] = useState(false);
    const [error, setError] = useState("");
    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");
        try {
            const formData = new FormData(event.target as HTMLFormElement);
            formData.append("accepted_privacy", acceptedPrivacy.toString());
            formData.append("accepted_terms", acceptedTerms.toString());
            await registerAction(formData);
        }
        catch (caughtError: any) {
            setError(caughtError?.password1?.[0] || caughtError?.password2?.[0] || caughtError?.email?.[0] || caughtError?.username?.[0] || caughtError?.detail?.[0] || "Registration failed!");
        }
    };
    return (
        <>
            <div className = "min-h-screen flex items-center justify-center bg-main-compliment">
                <div className = "flex flex-col items-center gap-6">
                    <form onSubmit = {handleSubmit} className = "w-90 p-8 rounded-2xl shadow-2xl bg-ui">
                        <h1 className = "text-7xl text-white font-log-title mb-3">Register</h1>
                        {error && <p className = "text-3xl text-red-500 font-log-title mb-5">{error}</p>}
                        <input type = "username" name = "username" value = {username} onChange = {exception => setUsername(exception.target.value)} placeholder = "Username" className = "input-element" required/>
                        <input type = "email" name = "email" value = {email} onChange = {exception => setEmail(exception.target.value)} placeholder = "Email" className = "input-element" required/>
                        <input type = "password" name = "password1" value = {password1} onChange = {exception => setPassword1(exception.target.value)} placeholder = "Password" className = "input-element" required/>
                        <input type = "password" name = "password2" value = {password2} onChange = {exception => setPassword2(exception.target.value)} placeholder = "Verify Password" className = "input-element" required/>
                        <div className = "flex flex-col gap-2 mt-4">
                            <label className = "flex items-center gap-2">
                                <input type = "checkbox" checked = {acceptedPrivacy} onChange = {(e) => setAcceptedPrivacy(e.target.checked)} required />
                                I agree to the <a href = "/privacy-policy.html" target = "_blank" className = "underline">Privacy Policy</a>
                            </label>
                            <label className = "flex items-center gap-2">
                                <input type = "checkbox" checked = {acceptedTerms} onChange = {(e) => setAcceptedTerms(e.target.checked)} required />
                                I agree to the <a href = "/terms-of-service.html" target = "_blank" className = "underline">Terms of Service</a>
                            </label>
                            <p>By signing up, you confirm that you are at least 13 years of age.</p>
                        </div>
                        <div className="flex justify-end mt-4">
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

export default Register;