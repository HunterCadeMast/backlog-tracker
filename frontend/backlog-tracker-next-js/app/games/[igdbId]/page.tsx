"use client";
import {useEffect, useState} from "react";
import {useParams, useRouter} from "next/navigation";

const GameInfo = () => {
    const router = useRouter();
    const {igdbId} = useParams();
    const [game, setGame] = useState<any>(null);
    const [log, setLog] = useState<any>(null);
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
        .then(setGame)
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
        <div className = "p-6 text-white">
            <h1 className = "text-3xl font-bold">{game.game_title}</h1>
            {game.cover_artwork_link && (<img src = {game.cover_artwork_link} className = "w-48 mt-4" />)}
            {log ? (
                <div className = "mt-6 bg-gray-800 p-4 rounded space-y-2">
                    {!editing ? (
                        <>
                            <p>Status: {log.user_status}</p>
                            {log.user_rating !== null && <p>Rating: {log.user_rating}/10</p>}
                            {log.user_review && <p>Review: {log.user_review}</p>}
                            {log.user_playtime !== null && <p>Playtime: {log.user_playtime}h</p>}
                            {log.start_date && <p>Start date: {log.start_date}</p>}
                            {log.completion_date && <p>Completion date: {log.completion_date}</p>}
                            <p>100% Completion: {log.full_completion ? "Yes" : "No"}</p>
                            <button className = "mt-2 text-navbar" onClick = {() => setEditing(true)}>Edit Log</button>
                        </>
                    ) : (
                        <>
                            <select value = {editFields.user_status} onChange = {(x) => setEditFields({...editFields, user_status: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white">
                                <option value = "playing">Playing</option>
                                <option value = "paused">Paused</option>
                                <option value = "completed">Completed</option>
                                <option value = "backlog">Backlog</option>
                                <option value = "dropped">Dropped</option>
                            </select>
                            <input type = "number" min = {0} max = {10} placeholder = "Rating (1 - 10)" value = {editFields.user_rating} onChange = {(x) => setEditFields({...editFields, user_rating: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white w-24" />
                            <textarea placeholder = "Review" value = {editFields.user_review} onChange = {(x) => setEditFields({...editFields, user_review: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white w-full" />
                            <input type = "number" min = {0} placeholder = "Hours of Playtime" value = {editFields.user_playtime} onChange = {(x) => setEditFields({...editFields, user_playtime: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white w-32" />
                            <input type = "date" value = {editFields.start_date} onChange = {(x) => setEditFields({...editFields, start_date: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white" />
                            <input type = "date" value = {editFields.completion_date} onChange = {(x) => setEditFields({...editFields, completion_date: x.target.value})} className = "rounded-md border px-3 py-2 bg-gray-800 text-white" />
                            <label className = "flex items-center gap-2 mt-2"><input type = "checkbox" checked = {editFields.full_completion} onChange = {(x) => setEditFields({...editFields, full_completion: x.target.checked})} className = "w-4 h-4" />100% Completion</label>
                            <div className = "flex gap-2 mt-2">
                                <button className = "bg-navbar px-4 py-2 rounded text-gray-800" onClick = {saveLog}>Save Edits</button>
                                <button className = "bg-gray-600 px-4 py-2 rounded" onClick = {() => setEditing(false)}>Cancel Edits</button>
                            </div>
                        </>
                    )}
                    <button className = "mt-2 bg-grey-800 px-4 py-2 rounded text-white" onClick = {removeLog}>Remove from Backlog</button>
                </div>
            ) : (
                <button className = "mt-6 bg-navbar px-4 py-2 rounded text-gray-800" onClick = {addLog}>Add to Backlog</button>
            )}
        </div>
    );
};

export default GameInfo;
