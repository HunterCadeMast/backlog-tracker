import type {Metadata} from "next";
import {Bebas_Neue, PT_Serif} from "next/font/google"
import localFont from "next/font/local"
import "./globals.css";
import ClientProvider from "../components/ClientProvider";
import RandomColor from "../components/RandomColor";

export const metadata: Metadata = {
  title: "Gaming Logjam - Backlog Tracker",
  description: "Track your video game backlog with UI and terminal interface",
};

const bebasNeue = Bebas_Neue({subsets: ["latin"], weight: "400", variable: "--font-bebasneue"});
const ptSerif = PT_Serif({subsets: ["latin"], weight: "400", variable: "--font-ptserif"});
const sekuya = localFont({src: "./fonts/Sekuya-Regular.ttf", weight: "400", variable: "--font-sekuya"})

export const dynamic = "force-dynamic";

export default function RootLayout({children}: Readonly<{children: React.ReactNode;}>) {
  return (
    <html lang = "en" className = {`${bebasNeue.variable} ${ptSerif.variable} ${sekuya.variable}`}>
      <body>
        <ClientProvider>
        <main className = "pt-16 h-screen flex flex-col">
          <div className = "flex-1">
            {children}
          </div>
          <footer className = "pl-10 pr-10 pb-5 flex items-center justify-between text-center bg-main-compliment">
            <h1 className = "font-main-title text-3xl text-white"><RandomColor>Database from IGDB</RandomColor></h1>
            <h1 className = "font-main-title text-xl text-white">Contact: <a href = "mailto:gaming.logjam@gmail.com" className = "underline"><RandomColor>gaming.logjam@gmail.com</RandomColor></a></h1>
          </footer>
        </main>
        </ClientProvider>
      </body>
    </html>
  );
}