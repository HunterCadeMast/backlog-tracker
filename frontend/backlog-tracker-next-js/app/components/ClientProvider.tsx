"use client";
import { AuthenticationContextProvider } from "@/src/lib/authentication";
import NavigationPanel from "./navigation";

export default function ClientProvider({children}: {children: React.ReactNode;}) {
  return (
    <AuthenticationContextProvider>
        <NavigationPanel />
        {children}
    </AuthenticationContextProvider>
  );
}