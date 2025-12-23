"use server";
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
        await apiFetch("/authentication/register/", {
            method: "POST",
            body: JSON.stringify({username, email, password: password1}),
        });
        const user = await apiFetch("/authentication/profile/");
        return user;
    }
    catch (error: any) {
        throw error;
    }
};
