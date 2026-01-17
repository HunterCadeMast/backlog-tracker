"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import RandomColor from "../../components/RandomColor";

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
            <div className="base-background pl-5 pr-5 pt-10">
                <div className = "grid grid-cols-1 lg:grid-cols-2 gap-10 items-center justify-between">
                    <div className = "space-y-6">
                        <section className = "bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className = "text-3xl font-main-title">Edit Profile</h1></RandomColor>
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title">Display Name</label>
                                <input placeholder = "Display Name" value = {profile.display_name} onChange = {(x) => setProfile({...profile, display_name: x.target.value})} className = "btn w-full mt-3" />
                            </div>
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title">Bio</label>
                                <textarea placeholder = "Bio" value = {profile.bio} onChange = {(x) => setProfile({...profile, bio: x.target.value})} rows = {4} className = "btn w-full mt-3 min-h-20 max-h-80"></textarea>
                            </div>
                            <label className = "inline-flex items-center space-x-2">
                                <input type="checkbox" checked = {!profile.private_profile} onChange = {() => setProfile({...profile, private_profile: !profile.private_profile})} className = "form-checkbox" />
                                <span>Public Profile</span>
                            </label>
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title pr-5">Profile Photo</label>
                                <input type = "file" accept = "image/*" onChange = {(x) => setProfilePhoto(x.target.files?.[0] ?? null)} />
                            </div>
                            <div className = "flex gap-4 mt-4">
                                <RandomColor element = "bg"><button onClick = {save} className = "btn px-4 py-2">Save Edits</button></RandomColor>
                                <RandomColor element = "bg"><button onClick = {() => router.push("/profile/")} className = "btn px-4 py-2">Cancel Edits</button></RandomColor>
                            </div>
                        </section>
                    </div>
                    <div className = "space-y-6">
                        <section className = "bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className = "text-xl font-main-title">Change Email</h1></RandomColor>
                            <input type = "email" placeholder = "New Email" value = {profile.email} onChange = {(x) => setProfile({...profile, email: x.target.value})} className = "btn w-full mt-3" />
                            <input type = "password" placeholder = "Current Password" value = {currentPassword} onChange = {(x) => setCurrentPassword(x.target.value)} className = "btn w-full mt-3" />
                            <RandomColor element = "bg"><button onClick = {emailChange} className = "btn px-4 py-2">Change Email</button></RandomColor>
                        </section>
                        <section className="bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className="text-xl font-main-title">Change Password</h1></RandomColor>
                            <div className = "grid grid-cols-1 gap-4">
                                <input type = "password" placeholder = "Current Password" value = {currentPassword} onChange = {(x) => setCurrentPassword(x.target.value)} className = "btn w-full" />
                                <input type = "password" placeholder = "New Password" value = {newPassword} onChange = {(x) => setNewPassword(x.target.value)} className = "btn w-full" />
                                <input type = "password" placeholder = "Confirm New Password" value = {confirmPassword} onChange = {(x) => setConfirmPassword(x.target.value)} className = "btn w-full" />
                            </div>
                            <RandomColor element = "bg">
                                <button onClick = {passwordChange} className = "btn px-4 py-2">Change Password</button>
                            </RandomColor>
                        </section>
                        <section>
                            <button onClick = {deleteAccount} className="btn px-6 py-2 hover:bg-red-500 transition-colors">Delete Account</button>
                        </section>
                    </div>
                </div>
            </div>
        );
    }
};

export default ProfileEdit;