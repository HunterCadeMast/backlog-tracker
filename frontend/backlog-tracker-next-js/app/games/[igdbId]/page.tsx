"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

const GameInfo = () => {
    const router = useRouter();
    const {igdbId} = useParams();
    const [game, setGame] = useState<any>(null);
    useEffect(() => {
    if (!igdbId) return;
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/games/${igdbId}/`).then(res => {
        if (!res.ok) {
            router.push("/not-found/");
            return;
        }
        return res.json();
    }).then(setGame).catch(err => {
        console.error(err);
        setGame(null);
    });
    }, [igdbId]);
    if (!game) return <p>Loading...</p>;
    return (
    <div className="p-6 text-white">
        <h1 className="text-3xl font-bold">{game.game_title}</h1>
        {game.cover_artwork_link && (<img src={game.cover_artwork_link} className="w-48 mt-4" />)}
    </div>
    );
};

export default GameInfo;