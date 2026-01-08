"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

const ProfileEdit = () => {
    const router = useRouter();
    const [profile, setProfile] = useState<any>(null);
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    useEffect(() => {
        apiFetch("/authentication/profile/").then(setProfile);
    }, []);
    async function passwordChange() {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/password/change/`, {method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}` }, body: JSON.stringify({ current_password: currentPassword, new_password: newPassword, new_password_confirm: confirmPassword }),});
        const data = await response.json();
        alert(data.message || data.error);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        router.push("/login");
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
                <section>
                    <h1>Edit Profile</h1>
                    <input placeholder = "Display Name" value = {profile.display_name} onChange = {x => setProfile({...profile, display_name: x.target.value})} />
                    <textarea placeholder = "Bio" value = {profile.bio} onChange = {x => setProfile({...profile, bio: x.target.value})}></textarea>
                    <label>
                        <input type = "checkbox" checked = {!profile.private_profile} onChange = {x => setProfile({...profile, private_profile: !profile.private_profile})} />Public Profile
                    </label>
                    <button onClick = {save}>Save Changes</button>
                    <button onClick = {cancel}>Cancel Changes</button>
                </section>
                <section>
                    <h1>Change Password</h1>
                    <input type = "password" placeholder = "Current Password" value = {currentPassword} onChange = {event => setCurrentPassword(event.target.value)} />
                    <input type = "password" placeholder = "New Password" value = {newPassword} onChange = {event => setNewPassword(event.target.value)} />
                    <input type = "password" placeholder = "Confirm new password" value = {confirmPassword} onChange = {event => setConfirmPassword(event.target.value)} />
                    <button onClick = {passwordChange}>Change Password</button>
                </section>
                <section>
                    <button onClick = {deleteAccount}>Delete Account</button>
                </section>
            </div>
        );
    }
};

export default ProfileEdit;