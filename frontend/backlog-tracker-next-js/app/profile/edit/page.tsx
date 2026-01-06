"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

const ProfileEdit = () => {
    const [profile, setProfile] = useState<any>(null);
    const router = useRouter();
    useEffect(() => {
        apiFetch("/authentication/profile/").then(setProfile);
    }, []);
    async function passwordChange(currentPassword: string, newPassword: string, confirmPassword: string) {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/password/change/`, {method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}` }, body: JSON.stringify({ current_password: currentPassword, new_password: newPassword, new_password_confirm: confirmPassword }),});
        const data = await response.json();
        alert(data.message || data.error);
    };
    async function deleteAccount() {
        if (!confirm("Are you sure you want to delete your Gaming Logjam account?")) return;
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/account/`, {method: "DELETE", headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },});
        localStorage.clear();
        router.push("/");
    };
    async function save() {
        await apiFetch("/authentication/profile/", {
            method: "PATCH",
            body: JSON.stringify(profile),
        });
        alert("Edits saved!");
        router.push("/profile/");
    };
    async function cancel() {
        router.push("/profile/");
    };
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div>
                <h1>Edit Profile</h1>
                <input value = {profile.display_name} onChange = {x => setProfile({...profile, display_name: x.target.value})} />
                <textarea value = {profile.bio} onChange = {x => setProfile({...profile, bio: x.target.value})}></textarea>
                <label>
                    <input type = "checkbox" checked = {!profile.private_profile} onChange = {x => setProfile({...profile, private_profile: !profile.private_profile})} />Public Profile
                </label>
                <button onClick = {save}>Save Changes</button>
                <button onClick = {cancel}>Cancel Changes</button>
            </div>
        );
    }
};

export default ProfileEdit;