"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";

const Users = () => {
    const router = useRouter();
    const { username } = useParams();
    const [profile, setProfile] = useState<any>(null);
    const [info, setInfo] = useState<any>(null);
    const [error, setError] = useState(false);
    useEffect(() => {
        apiFetch(`/profiles/${username}/`)
            .then(setProfile)
            .catch(() => setError(true));
    }, [username]);
    useEffect(() => {
        apiFetch("/profiles/personal/").then(setInfo);
    }, []);
    if (error) return router.push("/not-found");
    if (!profile) return <h1>Loading...</h1>;
    return (
        <div className="max-w-xl mx-auto p-6">
            {info?.profile_photo_url && (<img src = {info.profile_photo} className = "w-32 h-32 rounded-full mx-auto" alt = "Profile Photo" />)}
            <h1 className = "text-2xl text-center mt-4">{profile.display_name || profile.username}</h1>
            {profile.bio && (<p className = "text-center mt-2">{profile.bio}</p>)}
            {info?.statistics && (
                <section className = "mt-6">
                    <h1 className = "text-xl mb-2">Statistics</h1>
                    <p>Completed: {info.statistics.completed_games}</p>
                    <p>Playing: {info.statistics.playing_games}</p>
                    <p>Backlog: {info.statistics.backlog_games}</p>
                    <p>Dropped: {info.statistics.dropped_games}</p>
                    <p>Paused: {info.statistics.paused_games}</p>
                </section>
            )}
        </div>
    );
};

export default Users;