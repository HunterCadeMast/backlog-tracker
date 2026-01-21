"use client";

export async function loginAction(formData: FormData) {
    const email = formData.get('email');
    const password = formData.get('password');
    if (!email || !password) {
        throw {non_field_errors: ["Email and password are required!"]};
    }
    try {
        const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/login/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, password}),
        });
        const data = await loginResponse.json();
        if (!loginResponse.ok) {
            throw data
        }
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        return data.user;
    }
    catch (error: any) {
        if (error.non_field_errors) {
            throw error;
        }
        else {
            throw {non_field_errors: [error.error || error.detail || "Login failed!"]};
        }
    }
};
