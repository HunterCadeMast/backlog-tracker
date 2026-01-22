import { apiFetch } from "./api";

export async function userFetch() {
    try {
        return await apiFetch("/authentication/profile/");
    }
    catch {
        return null;
    }
};