"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import RandomColor from "@/components/RandomColor";

const STATUS_ORDER = ["playing", "paused", "completed", "backlog", "dropped"];

const Backlog = () => {
    const [logs, setLogs] = useState<any[]>([]);
    const [filters, setFilters] = useState({games: "", developers: "", publishers: "", genres: "", platforms: "", franchises: "", series: "", sort_user_logs: "status_ascending",});
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
            .then(data => setLogs(Array.isArray(data) ? data : data.logs || []))
            .catch(error => console.error("Cannot get logs!", error));
    }, [filters]);
    const handleFilterChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFilters({...filters, [event.target.name]: event.target.value});
    };
    const isStatusSort = filters.sort_user_logs === "status_ascending" || filters.sort_user_logs === "status_descending";
    const statusOrder =
    filters.sort_user_logs === "status_descending" ? [...STATUS_ORDER].reverse() : STATUS_ORDER;
    const groupedLogs = statusOrder.map(status =>
        logs.filter(log => log.user_status === status)
    );
    const flatSortedLogs = [...logs].sort((a, b) => {
        switch (filters.sort_user_logs) {
            case "rating_ascending":
                return (a.user_rating ?? 0) - (b.user_rating ?? 0);
            case "rating_descending":
                return (b.user_rating ?? 0) - (a.user_rating ?? 0);
            case "playtime_ascending":
                return (a.user_playtime ?? 0) - (b.user_playtime ?? 0);
            case "playtime_descending":
                return (b.user_playtime ?? 0) - (a.user_playtime ?? 0);
            default:
                return 0;
        }
    });
    return (
        <div className = "bg-main-compliment p-4 sm:p-8 md:p-16 min-h-screen">
            <div className = "fixed top-20 sm:top-29 left-0 right-0 z-25 px-4 sm:px-16 pt-4 pb-3 flex flex-wrap gap-4 items-center bg-main-compliment">
                <h1 className = "text-3xl font-main-title w-full">Backlog</h1>
                <input type = "text" placeholder = "Search games..." name = "games" value = {filters.games} onChange = {handleFilterChange} className = "btn px-3 py-2 w-full sm:w-72 md:w-96 bg-ui" />
                <select name = "sort_user_logs" value = {filters.sort_user_logs} onChange = {handleFilterChange} className = "btn px-3 py-2 bg-ui">
                    <option value = "status_ascending">Status (Ascending)</option>
                    <option value = "status_descending">Status (Descending)</option>
                    <option value = "rating_ascending">Rating (Ascending)</option>
                    <option value = "rating_descending">Rating (Descending)</option>
                    <option value = "playtime_ascending">Playtime (Ascending)</option>
                    <option value = "playtime_descending">Playtime (Descending)</option>
                </select>
            </div>
            <div className = "mt-45 sm:mt-30">
                {logs.length === 0 ? (<p className = "px-4 py-2 text-2xl text-white font-log-title">Hmm... Nothing to see here...</p>) : 
                isStatusSort ? (
                    groupedLogs.map((total_logs, index) => {
                        if (!total_logs.length) return null;
                        const current_status = statusOrder[index];
                        return (
                            <div key = {current_status} className = "mb-10">
                                <h2 className = "text-3xl font-main-title"><RandomColor constant>{current_status}</RandomColor></h2> 
                                <div className = "mt-4 space-y-6">
                                    {total_logs.map(log => (
                                        <RandomColor key = {log.id} element = "bg">
                                            <Link href = {`/games/${log.game.id}`} className = "p-4 bg-ui rounded-lg outline-4 outline-white flex flex-col md:flex-row gap-4 md:gap-6 transition">
                                                {log.game.cover_artwork_link ? (
                                                    <img src = {log.game.cover_artwork_link} alt = {log.game.game_title} className = "w-full sm:w-50 md:w-60 rounded-lg outline-4 outline-white" />
                                                ) : (
                                                    <img src = "/images/missing.jpg" alt = "Missing" className = "w-full sm:w-50 md:w-60 rounded-lg outline-4 outline-white" />
                                                )}
                                                <div className = "flex-1">
                                                    <p className = "text-3xl font-main-title mb-3">{log.game.game_title}</p>
                                                    <div className = "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-8">
                                                        <div className = "space-y-3">
                                                            <h1 className = "text-xl sm:text-2xl font-main-title">Status:</h1>
                                                            <p className = "text-xl indent-5">{log.user_status}</p>
                                                            {log.user_rating !== null && (
                                                                <>
                                                                    <h1 className = "text-xl sm:text-2xl font-main-title">Rating:</h1>
                                                                    <p className = "text-xl indent-5">{log.user_rating}/10</p>
                                                                </>
                                                            )}
                                                            {log.user_playtime !== null && (
                                                                <>
                                                                    <h1 className = "text-xl sm:text-2xl font-main-title">Playtime:</h1>
                                                                    <p className = "text-xl indent-5">{log.user_playtime} Hours</p>
                                                                </>
                                                            )}
                                                        </div>
                                                        <div className = "space-y-3">
                                                            {log.start_date && (
                                                                <>
                                                                    <h1 className = "text-xl sm:text-2xl font-main-title">Start Date:</h1>
                                                                    <p className = "text-xl indent-5">{log.start_date}</p>
                                                                </>
                                                            )}
                                                            {log.completion_date && (
                                                                <>
                                                                    <h1 className = "text-xl sm:text-2xl font-main-title">Completion Date:</h1>
                                                                    <p className = "text-xl indent-5">{log.completion_date}</p>
                                                                </>
                                                            )}
                                                            <h1 className = "text-xl sm:text-2xl font-main-title">100% Completion:</h1>
                                                            <p className = "text-xl indent-5">{log.full_completion ? "Yes" : "No"}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </Link>
                                        </RandomColor>
                                    ))}
                                </div>
                            </div>
                        );
                    })
                ) : (
                    <div className = "space-y-6">
                        {flatSortedLogs.map(log => (
                            <RandomColor key = {log.id} element = "bg">
                                <Link href = {`/games/${log.game.id}`} className = "p-4 bg-ui rounded-lg outline-4 outline-white flex flex-col md:flex-row gap-4 md:gap-6 transition">
                                    {log.game.cover_artwork_link ? (
                                        <img src = {log.game.cover_artwork_link} alt = {log.game.game_title} className = "w-30 rounded-lg outline-4 outline-white" />
                                    ) : (
                                        <img src = "/images/missing.jpg" alt = "Missing" className = "w-30 rounded-lg outline-4 outline-white" />
                                    )}
                                    <div className = "flex-1">
                                        <p className = "text-xl sm:text-2xl font-main-title mb-3">{log.game.game_title}</p>
                                        <div className = "grid grid-cols-2 gap-x-8 gap-y-4">
                                            <div className = "space-y-3">
                                                <h1 className = "text-xl sm:text-2xl font-main-title">Status:</h1>
                                                <p className = "text-xl indent-5">{log.user_status}</p>
                                                {log.user_rating !== null && (
                                                    <>
                                                        <h1 className = "text-xl sm:text-2xl font-main-title">Rating:</h1>
                                                        <p className = "text-xl indent-5">{log.user_rating}/10</p>
                                                    </>
                                                )}
                                                {log.user_playtime !== null && (
                                                    <>
                                                        <h1 className = "text-xl sm:text-2xl font-main-title">Playtime:</h1>
                                                        <p className = "text-xl indent-5">{log.user_playtime} Hours</p>
                                                    </>
                                                )}
                                            </div>
                                            <div className = "space-y-3">
                                                {log.start_date && (
                                                    <>
                                                        <h1 className = "text-xl sm:text-2xl font-main-title">Start Date:</h1>
                                                        <p className = "text-xl indent-5">{log.start_date}</p>
                                                    </>
                                                )}
                                                {log.completion_date && (
                                                    <>
                                                        <h1 className = "text-xl sm:text-2xl font-main-title">Completion Date:</h1>
                                                        <p className = "text-xl indent-5">{log.completion_date}</p>
                                                    </>
                                                )}
                                                <h1 className = "text-xl sm:text-2xl font-main-title">100% Completion:</h1>
                                                <p className="text-xl indent-5">{log.full_completion ? "Yes" : "No"}</p>
                                            </div>
                                        </div>
                                    </div>
                                </Link>
                            </RandomColor>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Backlog;