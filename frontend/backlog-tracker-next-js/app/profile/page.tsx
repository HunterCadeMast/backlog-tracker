"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { PieChart, Pie, Tooltip, ResponsiveContainer } from "recharts";

type ProfileStatisticsTypes = {
    completed_games: number;
    playing_games: number;
    backlog_games: number;
    dropped_games: number;
    paused_games: number;
};

type ProfileTypes = {
    username: string;
    display_name: string;
    bio: string;
    private_profile: boolean;
    profile_photo: string | null;
    statistics: ProfileStatisticsTypes | null;
};

const Profile = () => {
    const [profile, setProfile] = useState<ProfileTypes>({
        username: "",
        display_name: "",
        bio: "",
        private_profile: false,
        profile_photo: null,
        statistics: null,
    });
    useEffect(() => {
        Promise.all([
            apiFetch("/authentication/profile/"),
            apiFetch("/profiles/personal/"),
        ]).then(([auth, profile]) => {
            setProfile({
                username: auth.username,
                display_name: profile?.display_name ?? auth.username,
                bio: profile?.bio ?? "",
                private_profile: profile?.private_profile ?? false,
                profile_photo: profile?.profile_photo ?? null,
                statistics: profile?.statistics ?? null,
            });
        });
    }, []);
    const data = profile.statistics
        ? [
            { name: "Completed", value: profile.statistics.completed_games },
            { name: "Playing", value: profile.statistics.playing_games },
            { name: "Backlog", value: profile.statistics.backlog_games },
            { name: "Dropped", value: profile.statistics.dropped_games },
            { name: "Paused", value: profile.statistics.paused_games },
        ]
        : [];
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div>
                <h1>Name: {profile.display_name || profile.username}</h1>
                {profile.bio && <p>Bio: {profile.bio}</p>}
                <p>Visibility: {profile.private_profile ? "Private" : "Public"}</p>
                {profile.profile_photo && (<img src = {profile.profile_photo} alt = "Profile Photo" className = "w-32 h-32 rounded-full object-cover" />)}
                {profile.statistics && (
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