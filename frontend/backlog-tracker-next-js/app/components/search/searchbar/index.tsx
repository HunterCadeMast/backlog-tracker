"use client";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

type GameTypes = {
    id: string;
    game_title: string;
    cover_artwork_link?: string;
};

const SearchBar = () => {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<GameTypes[]>([]);
    const containerReference = useRef<HTMLDivElement>(null);
    const router = useRouter();
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
        const timer = setTimeout(async () => {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/games/?search=${encodeURIComponent(query)}`);
            const data = await response.json();
            if (Array.isArray(data)) {
                setResults(data);
            }
            if (data.results && Array.isArray(data.results)) {
                setResults(data.results);
            }
            else {
                setResults([]);
            }
        }, 300);
        return () => clearTimeout(timer);
    }, [query]);
    function handleSelect(game: GameTypes) {
        setOpen(false);
        setQuery("");
        router.push(`/games/${game.id}`);
    };
    return (
        <div ref = {containerReference} className = "relative w-72">
            <input type = "text" placeholder = "Search games..." onFocus = {() => setOpen(true)} value = {query} onChange = {(x) => setQuery(x.target.value)} className = "w-full rounded-md border px-3 py-2 bg-gray-800 text-white"/>
            {open && (
                <div className = "fixed top-15 left-5 right-5 z-50 mt-20 rounded-md bg-gray-800 text-white min-h-100 overflow-y-auto shadow-lg">
                    {results.length === 0 && query && (<p className = "px-4 py-2 text-sm text-white">Hmm... Nothing to see here...</p>)}
                    {results.map((game) => (
                        <button key = {game.id} onClick = {() => handleSelect(game)} className = "flex w-full items-center gap-3 px-4 py-2 hover:bg-gray-600 text-left">
                            {game.cover_artwork_link && (<img src = {game.cover_artwork_link} alt = {game.game_title} className = "h-10 w-7 rounded object-cover"/>)}
                            <span>{game.game_title}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchBar;