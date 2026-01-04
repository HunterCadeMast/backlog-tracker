"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

const STATUS_ORDER = ["playing", "paused", "completed", "backlog", "dropped"];

const Backlog = () => {
    const [logs, setLogs] = useState<any[]>([]);
    const [filters, setFilters] = useState({games: "", developers: "", publishers: "", genres: "", platforms: "", franchises: "", series: "", sort_user_logs: "",});
    useEffect(() => {
        const token = localStorage.getItem("access");
        if (!token) {
            return;
        }
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/?${params.toString()}`, {headers: { Authorization: `Bearer ${token}` },})
            .then(response => response.json())
            .then(data => setLogs(data))
            .catch(error => console.error("Cannot get logs!", error));
    }, [filters]);
    const handleFilterChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFilters({...filters, [event.target.name]: event.target.value});
    };
    const sortedLogs = STATUS_ORDER.map(current_status => logs.filter(log => log.user_status === current_status));
    return (
        <div className = "p-6 text-white">
            <h1 className = "text-3xl font-bold mb-4">Backlog</h1>
            <div className = "flex flex-wrap gap-4 mb-6">
                <input type = "text" placeholder = "Search games..." name = "games" value = {filters.games} onChange = {handleFilterChange} className = "rounded-md border px-3 py-2 bg-gray-800 text-white" />
                <select name = "sort_user_logs" value = {filters.sort_user_logs} onChange = {handleFilterChange} className = "rounded-md border px-3 py-2 bg-gray-800 text-white">
                    <option value = "">Sort By current_status</option>
                    <option value = "rating_ascending">Rating (Ascending)</option>
                    <option value = "rating_descending">Rating (Descending)</option>
                    <option value = "playtime_ascending">Playtime (Ascending)</option>
                    <option value = "playtime_descending">Playtime (Descending)</option>
                    <option value = "status_ascending">current_status (Ascending)</option>
                    <option value = "status_descending">current_status (Descending)</option>
                </select>
            </div>
            {sortedLogs.map((total_logs, index) => {
                if (total_logs.length === 0) {
                    return null;
                }
                const current_status = STATUS_ORDER[index];
                return (
                    <div key = {current_status} className = "mb-6">
                        <h2 className = "text-3xl">{current_status}</h2>
                        <div className = "mt-2 space-y-2">
                            {total_logs.map(log => (
                                <Link key = {log.id} href = {`/games/${log.game.id}`} className = "p-4 bg-gray-800 rounded flex items-center gap-4 hover:bg-gray-700 transition">
                                    {log.game.cover_artwork_link && (<img src = {log.game.cover_artwork_link} alt = {log.game.game_title} className = "w-24 h-24 object-cover rounded" />)}
                                    <div>
                                        <p className = "text-2xl">{log.game.game_title}</p>
                                        <p>Rating: {log.user_rating ?? "—"}/10</p>
                                        <p>Playtime: {log.user_playtime ?? 0} Hours</p>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default Backlog;
