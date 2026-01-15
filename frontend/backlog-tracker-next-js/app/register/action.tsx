"use client";
import { apiFetch } from "@/lib/api";

export async function registerAction(formData: FormData) {
    const username = formData.get('username');
    const email = formData.get('email');
    const password1 = formData.get('password1');
    const password2 = formData.get('password2');
    if (!username || !email || !password1 || !password2) {
        throw new Error("Username, email, and a password are required!")
    }
    if (password1 != password2) {
        throw new Error("Passwords do not match!")
    }
    try {
        const registerResponse = await apiFetch("/authentication/register/", {
            method: "POST",
            body: JSON.stringify({username, email, password: password1, accepted_privacy: formData.get("accepted_privacy") === "true", accepted_terms: formData.get("accepted_terms") === "true",}),
            headers: {
                "Content-Type": "application/json",
            },
        });
        localStorage.setItem("access", registerResponse.access);
        localStorage.setItem("refresh", registerResponse.refresh);
        return registerResponse.user;
    }
    catch (error: any) {
        throw error;
    }
};
