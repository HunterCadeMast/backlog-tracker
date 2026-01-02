import type { Metadata } from "next";
import {Bebas_Neue, PT_Serif} from "next/font/google"
import localFont from "next/font/local"
import "./globals.css";
import ClientProvider from "./components/ClientProvider";

export const metadata: Metadata = {
  title: "Gaming Logjam - Backlog Tracker",
  description: "Track your video game backlog with UI and terminal interface",
};

const bebasNeue = Bebas_Neue({subsets: ["latin"], weight: "400", variable: "--font-bebasneue"});
const ptSerif = PT_Serif({subsets: ["latin"], weight: "400", variable: "--font-ptserif"});
const sekuya = localFont({src: "./fonts/Sekuya-Regular.ttf", weight: "400", variable: "--font-sekuya"})

export default function RootLayout({children}: Readonly<{children: React.ReactNode;}>) {
  return (
    <html lang="en" className = { `${bebasNeue.variable} ${ptSerif.variable} ${sekuya.variable}` }>
      <body>
        <ClientProvider>
          {children}
        </ClientProvider>
        <div className = "flex items-center justify-between bg-cream">
          <h1 className = "ml-10 font-main-title text-3xl text-gray-800">Database from IGDB</h1>
        </div>
      </body>
    </html>
  );
}