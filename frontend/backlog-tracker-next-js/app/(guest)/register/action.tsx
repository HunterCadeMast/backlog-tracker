"use client";

export async function registerAction(formData: FormData) {
    const username = formData.get('username');
    const email = formData.get('email');
    const password1 = formData.get('password1');
    const password2 = formData.get('password2');
    if (!username || !email || !password1 || !password2) {
        throw {non_field_errors: ["All fields are required!"]};
    }
    if (password1 != password2) {
        throw {password2: ["Passwords do not match!"]};
    }
    try {
        const registerResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/register/`, {
            method: "POST",
            body: JSON.stringify({username, email, password: password1, accepted_privacy: formData.get("accepted_privacy") === "true", accepted_terms: formData.get("accepted_terms") === "true",}),
            headers: {"Content-Type": "application/json",},
        });
        const data = await registerResponse.json();
        if (!registerResponse.ok) {
            throw data
        }
        return data;
    }
    catch (error: any) {
        if (error.username || error.email || error.password2 || error.non_field_errors) {
            throw error;
        }
        throw {non_field_errors: [error?.message || "Registration failed!"]};
    }
};
