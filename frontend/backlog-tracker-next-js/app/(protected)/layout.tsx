"use client";
import UserAuthentication from "../components/UserAuthentication";

export default function ProtectedLayout({children,}: {children: React.ReactNode;}) {
    return <UserAuthentication>{children}</UserAuthentication>;
};