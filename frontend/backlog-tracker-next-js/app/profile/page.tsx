"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { PieChart, Pie, Tooltip, ResponsiveContainer } from "recharts";

const Profile = () => {
    const [profile, setProfile] = useState<any>(null);
    const [stats, setStats] = useState<any>(null);
    useEffect(() => {
        apiFetch("/authentication/profile/").then(setProfile);
    }, []);
    useEffect(() => {
        apiFetch("/profiles/personal/").then(setStats);
    }, []);
    const data = stats
        ? [
            { name: "Completed", value: stats.statistics.completed_games },
            { name: "Playing", value: stats.statistics.playing_games },
            { name: "Backlog", value: stats.statistics.backlog_games },
            { name: "Dropped", value: stats.statistics.dropped_games },
            { name: "Paused", value: stats.statistics.paused_games },
        ]
        : [];
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div>
                <h1>Name: {profile.username}</h1>
                <p>Bio: {profile.bio}</p>
                <p>Visibility: {profile.private_profile ? "Private" : "Public"}</p>
                {stats && (
                    <ResponsiveContainer width = "100%" height = {300}>
                        <PieChart>
                            <Pie data = {data} dataKey = "value" nameKey = "name" />
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                )}
            </div>
        );
    }
};

export default Profile;