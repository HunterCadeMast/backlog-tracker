"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import RandomColor from "../../RandomColor";

type GameTypes = {
    id: string;
    game_title: string;
    cover_artwork_link?: string;
};

const SearchBar = () => {
    const router = useRouter();
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<GameTypes[]>([]);
    const containerReference = useRef<HTMLDivElement>(null);
    useEffect(() => {
        function handleClick(event: MouseEvent) {
            if (containerReference.current && !containerReference.current.contains(event.target as Node)) {
                setOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);
    useEffect(() => {
        if (!query.trim()) {
            setResults([]);
            return;
        }
        const controller = new AbortController();
        const timer = setTimeout(async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/games/?search=${encodeURIComponent(query)}`, { signal: controller.signal });
                if (!response.ok) {
                    router.push("/not-found");
                    return;
                }
                const data = await response.json();
                setResults(Array.isArray(data) ? data: Array.isArray(data.results) ? data.results: []);
            }
            catch (error: any) {
                if (error.name === "AbortError") {
                    return
                }
                console.error(error);
            }
        }, 300)
        return () => {
            controller.abort();
            clearTimeout(timer);
        };
    }, [query]);
    function handleSelect(game: GameTypes) {
        setOpen(false);
        setQuery("");
        router.push(`/games/${game.id}`);
    };
    async function log(game: GameTypes) {
        try {
            const token = localStorage.getItem("access");
            if (!token) {
                router.push("/login");
                return;
            }
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/backlog/`, {method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`,}, body: JSON.stringify({game_id: game.id, user_status: "backlog", }), });
            if (!response.ok) {
                throw new Error("Failed to log!");
            }
            setResults(prev => prev.map(game_log => game_log.id === game.id ? {...game_log, is_in_backlog:true} : game_log));
        }
        catch (error) {
            console.error(error);
        }
    };
    return (
        <div ref = {containerReference} className = "relative w-96">
            <input type = "text" placeholder = "Search games..." onFocus = {() => setOpen(true)} value = {query} onChange = {(x) => setQuery(x.target.value)} spellCheck = {false} className = "w-full btn px-4 py-3 placeholder:placehold"/>
            {open && (
                <div className = "absolute mt-5 w-full max-h-96 min-h-12 overflow-y-auto rounded-lg bg-ui shadow-lg z-50 outline-4 outline-button-border">
                    {results.length === 0 && query && (<p className = "px-4 py-2 text-2xl text-white font-log-title">Hmm... Nothing to see here...</p>)}
                    {results.map((game, index) => (
                        <RandomColor key = {`${game.id}-${index}`} element = "bg">
                            <button onClick = {() => handleSelect(game)} className = "flex w-full items-center gap-3 px-4 py-2 text-left text-white font-log-title">
                                {game.cover_artwork_link ? (
                                    <img src = {game.cover_artwork_link} alt = {game.game_title} className = "h-20 w-16 rounded-lg outline-4 outline-white object-cover"/>
                                ) : (
                                    <img src = "/images/missing.jpg" alt = "Missing" className = "w-16 rounded-lg outline-4 outline-white object-cover"/>
                                )}
                                <span className = "text-2xl">{game.game_title}</span>
                            </button>
                        </RandomColor>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchBar;