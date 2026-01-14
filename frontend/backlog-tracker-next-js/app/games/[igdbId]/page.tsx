"use client";
import {useEffect, useState} from "react";
import {useParams, useRouter} from "next/navigation";
import RandomColor from "../../components/RandomColor";

const GameInfo = () => {
    const router = useRouter();
    const {igdbId} = useParams();
    const [game, setGame] = useState<any>(null);
    const [log, setLog] = useState<any>(null);
    const [favorite, setFavorite] = useState(false);
    const [editing, setEditing] = useState(false);
    const [editFields, setEditFields] = useState<any>({});
    useEffect(() => {
        if (!igdbId) return;
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/games/${igdbId}/`)
        .then((response) => {
            if (!response.ok) {
                router.push(" /not-found");
                return;
           }
            return response.json();
        })
        .then((data) => {
            console.log("GAME:", data);
            setGame(data);
        })
        .catch((error) => {
            console.error(error);
            setGame(null);
       });
    }, [igdbId]);
    useEffect(() => {
        const token = localStorage.getItem("access");
        if (!token || !igdbId) return;
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/?igdb_id=${igdbId}`, {headers: {Authorization: `Bearer ${token}`},})
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                setLog(data[0]);
                setEditFields({user_status: data[0].user_status || "backlog", user_rating: data[0].user_rating ?? "", user_review: data[0].user_review ?? "", user_playtime: data[0].user_playtime ?? "", start_date: data[0].start_date ?? "", completion_date: data[0].completion_date ?? "", full_completion: data[0].full_completion ?? false,});
           }
       });
    }, [igdbId]);
    useEffect(() => {
        const token = localStorage.getItem("access");
        if (!token || !game) return;
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/profile/`, {headers: { Authorization: `Bearer ${token}` },})
        .then(response => response.json())
        .then(profile => {setFavorite(profile.favorite_game === game.game_title);});
    }, [game]);
    const toggleFavorite = async () => {
        const token = localStorage.getItem("access");
        if (!token || !game?.game_title) return;
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/profile/`, {method: "PATCH", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`,}, body: JSON.stringify({favorite_game: game.game_title}),});
        if (response.ok) {
            setFavorite(true);
            alert(`${game.game_title} is now your favorite!`);
        } 
        else {
            alert("Failed to set as favorite!");
        }
    };
    const addLog = async () => {
        const token = localStorage.getItem("access");
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/backlog/`, {method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`,}, body: JSON.stringify({game_id: igdbId, user_status: "backlog"}),});
        if (response.ok) {
            const data = await response.json();
            setLog(data);
            setEditFields({user_status: "backlog", user_rating: "", user_review: "", user_playtime: "", start_date: "", completion_date: "", full_completion: false,});
       }
    };
    const removeLog = async () => {
        if (!log) {
            return;
        }
        const token = localStorage.getItem("access");
        if (!token) {
            return;
        }
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/backlog/remove/?game_id=${igdbId}`, {method: "DELETE", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`},});
            if (response.status === 204) {
                alert("Removed log!");
                setLog(null);
                setEditFields({});
            }
            else {
                const data = await response.json();
                alert(data.error || "Remove log failed!");
            }
        }
        catch (error) {
            console.error("Cannot remove log!", error);
        }
    };
    const saveLog = async () => {
        if (!log?.id) return;
        const token = localStorage.getItem("access");
        const updates: any = {};
        if (editFields.user_status) {
            updates.user_status = editFields.user_status;
       }
        if (editFields.user_rating !== "") {
            updates.user_rating = Number(editFields.user_rating);
       }
        if (editFields.user_review !== "") {
            updates.user_review = editFields.user_review;
       }
        if (editFields.user_playtime !== "") {
            updates.user_playtime = Number(editFields.user_playtime);
       }
        if (editFields.start_date !== "") {
            updates.start_date = editFields.start_date;
       }
        if (editFields.completion_date !== "") {
            updates.completion_date = editFields.completion_date;
       }
        updates.full_completion = editFields.full_completion;
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/${log.id}/`, {method: "PATCH", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`,}, body: JSON.stringify(updates),});
            if (!response.ok) {
                const error = await response.text();
                console.error("Log update failed!", error);
                return;
           }
            const updated = await response.json();
            setLog(updated);
            setEditing(false);
       }
        catch (error) {
            console.error("Network error:", error);
       }
    };
    if (!game) return <p>Loading...</p>;
    return (
        <div className = "base-background">
            <div className = "flex-1 p-6">
                <div className = "grid grid-cols-[200px_1fr] gap-8 pt-12">
                    <div className = "space-y-4 pt-4 items-center">
                        <RandomColor constant><h1 className = "text-3xl font-main-title">{game.game_title}</h1></RandomColor>
                        {game.cover_artwork_link && (<img src = {game.cover_artwork_link} className = "w-48 mt-4 rounded-lg outline-4 outline-white" />)}
                        {!log && (<RandomColor element = "bg"><button className = "btn mt-6 bg-ui" onClick = {addLog}>Add to Backlog</button></RandomColor>)}
                    </div>
                    <div className = "space-y-4">
                        <p className = "break-up-line"></p>
                        <RandomColor constant><h1 className = "text-xl font-main-title">Summary:</h1></RandomColor>
                        <p className = "break-up-line indent-10"> {game.summary || "No description available..."}</p>
                        <div className="grid grid-cols-2 gap-6">
                            <div className = "space-y-2">
                                <div className = "space-y-2 pr-4 border-r border-white">
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Release Date:</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {game.release_date || "Unknown"}</p>
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Average Rating:</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {game.average_rating ?? "Unknown"}</p>
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Developer(s):</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {game.developers?.length ? game.developers.join(", ") : "Unknown"}</p>
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Publisher(s):</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {game.publishers?.length ? game.publishers.join(", ") : "Unknown"}</p>
                                </div>
                            </div>
                            <div className = "space-y-2">
                                <RandomColor constant><h1 className = "text-xl font-main-title">Genre(s):</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {game.genres?.length ? game.genres.join(", ") : "Unknown"}</p>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Platform(s):</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {game.platforms?.length ? game.platforms.join(", ") : "Unknown"}</p>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Franchise(s):</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {game.franchises?.length ? game.franchises.join(", ") : "Unknown"}</p>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Series:</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {game.series?.length ? game.series.join(", ") : "Unknown"}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {log && (
                    <div className = "h-[20vh] border-t rounded-lg outline-4 outline-white font-log-title text-white bg-ui p-6 ml-10 mr-10 mb-5">
                        {!editing ? (
                            <>
                                <p>Status: {log.user_status}</p>
                                {log.user_rating !== null && <p>Rating: {log.user_rating}/10</p>}
                                {log.user_review && <p>Review: {log.user_review}</p>}
                                {log.user_playtime !== null && <p>Playtime: {log.user_playtime}h</p>}
                                {log.start_date && <p>Start date: {log.start_date}</p>}
                                {log.completion_date && <p>Completion date: {log.completion_date}</p>}
                                <p>100% Completion: {log.full_completion ? "Yes" : "No"}</p>
                                <button className = "btn bg-ui" onClick = {() => setEditing(true)}>Edit Log</button>
                                <button className = "btn bg-ui" onClick = {removeLog}>Remove from Backlog</button>
                            </>
                        ) : (
                            <div className="grid grid-cols-6 gap-4">
                                <select value = {editFields.user_status} onChange = {(x) => setEditFields({...editFields, user_status: x.target.value})} className = "btn bg-ui w-50">
                                    <option value = "playing">Playing</option>
                                    <option value = "paused">Paused</option>
                                    <option value = "completed">Completed</option>
                                    <option value = "backlog">Backlog</option>
                                    <option value = "dropped">Dropped</option>
                                </select>
                                <input type = "number" min = {0} max = {10} placeholder = "Rating (1 - 10)" value = {editFields.user_rating} onChange = {(x) => setEditFields({...editFields, user_rating: x.target.value})} className = "btn w-45 bg-ui" />
                                <input type = "number" min = {0} placeholder = "Hours of Playtime" value = {editFields.user_playtime} onChange = {(x) => setEditFields({...editFields, user_playtime: x.target.value})} className = "btn w-65 bg-ui" />
                                <label className = "flex items-center gap-2 mt-2"><input type = "checkbox" checked = {editFields.full_completion} onChange = {(x) => setEditFields({...editFields, full_completion: x.target.checked})} className = "w-4 h-4" />100% Completion</label>
                                <input type = "date" value = {editFields.start_date} onChange = {(x) => setEditFields({...editFields, start_date: x.target.value})} className = "btn bg-ui" />
                                <input type = "date" value = {editFields.completion_date} onChange = {(x) => setEditFields({...editFields, completion_date: x.target.value})} className = "btn bg-ui" />
                                <textarea placeholder = "Review" value = {editFields.user_review} onChange = {(x) => setEditFields({...editFields, user_review: x.target.value})} className = "btn  text-whitew-full" />
                                {log && !favorite && (<button onClick = {toggleFavorite} className = "btn bg-ui">Set as Favorite</button>)}
                                {favorite && (<span className="px-4 py-2 rounded bg-ui text-white">Favorite Game</span>)}
                                <button className = "btn bg-ui" onClick = {saveLog}>Save Edits</button>
                                <button className = "btn bg-ui" onClick = {() => setEditing(false)}>Cancel Edits</button>
                            </div>
                        )}
                    </div>
                )}
        </div>
    );
};

export default GameInfo;
