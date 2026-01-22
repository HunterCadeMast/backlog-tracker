export function accessTokenFetch() {
    return localStorage.getItem("access");
};

export function refreshTokenFetch() {
    return localStorage.getItem("refresh");
};

export function setTokens(access_token: string, refresh_token: string) {
    localStorage.setItem("access", access_token);
    localStorage.setItem("refresh", refresh_token);
};

export function removeTokens() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
};

export function loggedInCheck() {
    return !!accessTokenFetch();
};