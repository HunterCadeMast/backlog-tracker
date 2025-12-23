"use client";
import { useEffect, useState } from "react";
import { userFetch } from "@/lib/authentication";

const Profile = () => {
    const [user, setUser] = useState<any>(null);
    useEffect(() => {
        async function user() {
            const account = await userFetch();
            setUser(account);
        }
        user();
    }, []);
    if (!user) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div>
                Profile
            </div>
        );
    }
};

export default Profile;