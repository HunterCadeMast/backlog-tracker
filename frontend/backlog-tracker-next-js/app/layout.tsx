import type { Metadata } from "next";
import {Bebas_Neue, PT_Serif} from "next/font/google"
import localFont from "next/font/local"
import NavigationPanel from "./components/navigation";
import "./globals.css";

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
        <NavigationPanel />
        {children}
      </body>
    </html>
  );
}