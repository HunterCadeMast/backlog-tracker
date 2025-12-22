"use server";
import { apiFetch } from "@/lib/api";

export async function logoutAction(formData: FormData) {
    await apiFetch("/accounts/logout/", {
        method: "POST",
    });
}