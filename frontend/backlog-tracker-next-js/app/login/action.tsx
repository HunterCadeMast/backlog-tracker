"use client";
import { apiFetch } from "@/lib/api";

export async function loginAction(formData: FormData) {
    const email = formData.get('email');
    const password = formData.get('password');
    if (!email || !password) {
        throw new Error("Email and password are required!")
    }
    try {
        const loginResponse = await apiFetch("/authentication/login/", {
            method: "POST",
            body: JSON.stringify({email, password}),
        });
        localStorage.setItem("access", loginResponse.access);
        localStorage.setItem("refresh", loginResponse.refresh);
        return loginResponse.user;
    }
    catch (error: any) {
        throw new Error(error?.error || "Login failed!")
    }
};
