"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

const Profile = () => {
    const [profile, setProfile] = useState<any>(null);
    useEffect(() => {
        apiFetch("/authentication/profile/").then(setProfile);
    }, []);
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div>
                <h1>Name: {profile.username}</h1>
                <p>Bio: {profile.bio}</p>
                <p>Visibility: {profile.private_profile ? "Private" : "Public"}</p>
            </div>
        );
    }
};

export default Profile;