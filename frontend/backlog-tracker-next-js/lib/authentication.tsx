"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { userFetch } from "./user";
import { removeTokens, accessTokenFetch  } from "./tokens";

type AuthenticationType = {
    user: any;
    loading: boolean;
    refreshUser: () => Promise<void>;
    logout: () => void;
};

const AuthenticationContext = createContext<AuthenticationType | null>(null);

export function AuthenticationContextProvider({children}: {children: React.ReactNode}) {
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const refreshUser = async () => {
        try {
            const access_token = accessTokenFetch();
            if (!access_token) {
                setUser(null);
                setLoading(false);
                return;
            }
            const account = await userFetch();
            setUser(account);
        } catch (error) {
            console.error("Failed to refresh user:", error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };
    const logout = () => {
        removeTokens();
        setUser(null);
    };
    useEffect(() => {
        refreshUser();
    }, []);
    return (
        <AuthenticationContext.Provider value = {{user, loading, refreshUser, logout}}>
            {children}
        </AuthenticationContext.Provider>
    );
};

export function useAuthentication() {
    const context = useContext(AuthenticationContext);
    if (!context) {
        throw new Error("Authentication must be inside of the provider!");
    }
    else {
        return context;
    }
};