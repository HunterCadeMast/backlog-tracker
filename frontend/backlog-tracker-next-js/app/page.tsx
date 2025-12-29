"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function Home() {
  return (
    <>
      <div className = "container max-w-screen min-h-screen mx-auto flex items-center justify-center bg-cream">
        <h1 className = "font-main-title text-9xl">Gaming Logjam</h1>
      </div>
    </>
  );
}
