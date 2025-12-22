"use server";
import { apiFetch } from "@/lib/api";

export async function loginAction(formData: FormData) {
    const email = formData.get('email');
    const password = formData.get('password');
    if (!email || !password) {
        throw new Error("Email and password are required!")
    }
    try {
        await apiFetch("/accounts/login/", {
            method: "POST",
            body: JSON.stringify({email, password}),
        });
        const user = await apiFetch("/accounts/profile/");
        return user;
    }
    catch (error: any) {
        throw new Error(error?.error || "Login failed!")
    }
};
