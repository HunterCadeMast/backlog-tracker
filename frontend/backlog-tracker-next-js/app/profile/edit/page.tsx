"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

const ProfileEdit = () => {
    const router = useRouter();
    const [profile, setProfile] = useState<any>(null);
    const [profilePhoto, setProfilePhoto] = useState<File | null>(null);
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    useEffect(() => {
        apiFetch("/profiles/personal/").then(data => {setProfile({display_name: data.display_name ?? "", bio: data.bio ?? "", private_profile: data.private_profile ?? false, email: data.email ?? "",});});
    }, []);
    async function passwordChange() {
        if (!currentPassword) {
            alert("Current password is empty!");
            return;
        }
        if (!newPassword) {
            alert("New password is empty!");
            return;
        }
        if (!confirmPassword) {
            alert("New password confirmation is empty!");
            return;
        }
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/password/change/`, {method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}` }, body: JSON.stringify({ current_password: currentPassword, new_password: newPassword, new_password_confirm: confirmPassword }),});
        const data = await response.json();
        alert(data.message || data.error);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        router.push("/login");
    };
    async function emailChange() {
        if (!profile.email) {
            alert("Email is empty!");
            return;
        }
        if (!currentPassword) {
            alert("Current password is empty!");
            return;
        }
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/email/change/`, {method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}` }, body: JSON.stringify({ current_password: currentPassword, email: profile.email }),});
        const data = await response.json();
        alert(data.message || data.error);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        router.push("/login");
    };
    async function deleteAccount() {
        if (!confirm("Are you sure you want to delete your Gaming Logjam account?")) return;
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/delete-account/`, {method: "DELETE", headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },});
        localStorage.clear();
        router.push("/");
    };
    async function save() {
        const formData = new FormData();
        formData.append("display_name", profile.display_name);
        formData.append("bio", profile.bio);
        formData.append("private_profile", profile.private_profile);
        if (profilePhoto) {
            formData.append("profile_photo", profilePhoto);
        }
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/profiles/personal/`, {method: "PATCH", headers: {Authorization: `Bearer ${localStorage.getItem("access")}`,}, body: formData,});
        alert("Profile edits saved!");
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
                    <input type="file" accept="image/*" onChange={(x) => setProfilePhoto(x.target.files?.[0] ?? null)} />
                    <button onClick = {save}>Save Changes</button>
                    <button onClick = {cancel}>Cancel Changes</button>
                </section>
                <section>
                    <h1>Change Email</h1>
                    <input type = "email" placeholder = "New Email" value = {profile.email} onChange={x => setProfile({...profile, email: x.target.value})} />
                    <input type = "password" placeholder = "Current Password" value = {currentPassword} onChange={x => setCurrentPassword(x.target.value)} />
                    <button onClick = {emailChange}>Change Email</button>
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