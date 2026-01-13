"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { PieChart, Pie, Tooltip, ResponsiveContainer } from "recharts";
import { useRouter } from "next/navigation";
import RandomColor from "../components/RandomColor";

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
    favorite_game: string | null,
    statistics: ProfileStatisticsTypes | null;
};

const Profile = () => {
    const router = useRouter();
    const [profile, setProfile] = useState<ProfileTypes>({
        username: "",
        display_name: "",
        bio: "",
        private_profile: false,
        profile_photo: null,
        favorite_game: null,
        statistics: null,
    });
    useEffect(() => {
        const token = localStorage.getItem("access");
        if (!token) {
            router.push("/not-found");
            return;
        }
        const fetchProfile = async () => {
            const authentication = await apiFetch("/authentication/profile/");
            const personal = await apiFetch("/profiles/personal/");
            setProfile({
                username: authentication.username,
                display_name: personal?.display_name ?? authentication.username,
                bio: personal?.bio ?? "",
                private_profile: personal?.private_profile ?? false,
                profile_photo: personal?.profile_photo ?? null,
                favorite_game: personal?.favorite_game ?? "No favorite game...",
                statistics: personal?.statistics ?? null,
            });
        };
        fetchProfile();
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
    const statisticColors = ["#EC4E20", "#FF9505", "#FC60A8", "#65DD65"];
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div className = "base-background pl-30">
                <h1 className="text-6xl font-main-title">
                    <RandomColor>{profile.display_name || profile.username}</RandomColor>
                </h1>
                <div className="flex flex-col md:flex-row gap-10 items-start">
                    {profile.profile_photo && (<img src = {profile.profile_photo} alt = "Profile Photo" className = "w-48 h-48 rounded-full object-cover" />)}
                    <div className="flex flex-col gap-4">
                        {profile.bio && (<p className = "text-2xl"><RandomColor><span className = "">Bio: </span></RandomColor>{profile.bio}</p>)}
                        {profile.favorite_game && <p className = "text-2xl"><RandomColor><span className = "">Favorite Game: </span></RandomColor>{profile.favorite_game}</p>}
                    </div>
                </div>
                <div className = "flex items-center gap-4 mt-4 mb-4">
                    <RandomColor element = "bg"><button onClick = {() => router.push("/profile/edit")} className = "px-4 py-2 btn">Edit Profile</button></RandomColor>
                </div>
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