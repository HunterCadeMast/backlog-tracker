"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function Home() {
  return (
    <>
      <div className = "container max-w-screen mx-auto">
        <h1 className = "font-main-title">Gaming Logjam</h1>
        <p className = "font-log-title">Hello world!</p>
        <div className = "w-full h-screen bg-cream"></div>
        <p className = "font-log-body">My favorite game is Final Fantasy X!</p>
      </div>
    </>
  );
}
