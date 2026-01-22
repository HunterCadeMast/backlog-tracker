"use client";
import UserGuest from "@/components/UserGuest";

export default function GuestLayout({children,}: {children: React.ReactNode;}) {
    return <UserGuest>{children}</UserGuest>;
};