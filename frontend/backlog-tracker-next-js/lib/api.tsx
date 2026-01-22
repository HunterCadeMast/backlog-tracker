import { accessTokenFetch, refreshTokenFetch, setTokens, removeTokens } from "./tokens";

export async function apiFetch(url: string, options: RequestInit = {}) {
    const access_token = await accessTokenFetch();
    const access_response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, {...options, headers: {"Content-Type": "application/json", ...(access_token ? {Authorization: `Bearer ${access_token}`} : {}), ...options.headers,},});
    if (access_response.status !== 401) {
        return access_response.json()
    }
    const refresh_token = await refreshTokenFetch();
    if (!refresh_token) {
        removeTokens();
        return Promise.reject("Not authenticated!");
    }
    const refresh_response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/refresh/`, {method: "POST", headers: {"Content-Type": "application/json",}, body: JSON.stringify({refresh: refresh_token}),});
    if (!refresh_response.ok) {
        removeTokens();
        throw new Error("Session expired!");
    }
    const tokens = await refresh_response.json();
    setTokens(tokens.access, tokens.refresh);
    return apiFetch(url, options);
};