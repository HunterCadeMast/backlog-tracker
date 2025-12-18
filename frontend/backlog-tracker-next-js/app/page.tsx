"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function Home() {
  return (
    <div>
      <h1 className = "font-main-title">Gaming Logjam</h1>
      <p className = "font-log-title">Hello world!</p>
      <div className = "bg-cream w-full h-screen">
        <p className = "font-log-body">My favorite game is Final Fantasy X!</p>
      </div>
    </div>
  );
}
