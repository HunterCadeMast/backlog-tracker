"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import RandomColor from "../../../components/RandomColor";

const ProfileEdit = () => {
    const router = useRouter();
    const [profile, setProfile] = useState<any>(null);
    const [profilePhoto, setProfilePhoto] = useState<File | null>(null);
    const [currentPasswordForEmail, setCurrentPasswordForEmail] = useState("");
    const [currentPasswordForPassword, setCurrentPasswordForPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [errors, setErrors] = useState<Record<string, string[]>>({});
    const [emailErrors, setEmailErrors] = useState<Record<string, string[]>>({});
    const [passwordErrors, setPasswordErrors] = useState<Record<string, string[]>>({});
    useEffect(() => {
        apiFetch("/profiles/personal/").then(data => {setProfile({username: data.username ?? "", bio: data.bio ?? "", private_profile: data.private_profile ?? false, email: data.email ?? "", has_password: data.has_password ?? false, providers: data.providers ?? [],});});
    }, []);
    async function passwordChange() {
        setPasswordErrors({});
        if ((profile.has_password && !currentPasswordForPassword) || !newPassword || !confirmPassword) {
            setPasswordErrors({non_field_errors: ["All fields are required!"]});
            return;
        }
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/password/change/`, {method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}`}, body: JSON.stringify({current_password: currentPasswordForPassword, new_password: newPassword, new_password_confirm: confirmPassword}),});
        const data = await response.json();
        if (!response.ok) {
            setPasswordErrors(data);
            return;
        }
        alert("Password changed successfully! Please login again...");
        localStorage.clear();
        router.push("/login");
    };
    async function emailChange() {
        setEmailErrors({});
        if (!profile.email || (profile.has_password && !currentPasswordForEmail)) {
            setEmailErrors({non_field_errors: ["Email and current password are required!"]});
            return;
        }
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/email/change/`, {method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}`}, body: JSON.stringify({current_password: currentPasswordForEmail, email: profile.email}),});
        const data = await response.json();
        if (!response.ok) {
            setEmailErrors(data);
            return;
        }
        alert("Email changed successfully! Please login again...");
        localStorage.clear();
        router.push("/login");
    };
    async function deleteAccount() {
        if (!confirm("Are you sure you want to delete your Gaming Logjam account?")) return;
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/delete-account/`, {method: "DELETE", headers: {Authorization: `Bearer ${localStorage.getItem("access")}`},});
        localStorage.clear();
        router.push("/");
    };
    async function unlinkAccount(provider: string) {
        if (!confirm(`Unlink ${provider}?`)) return;
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/authentication/oauthentication/unlinked/`, {method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("access")}`,}, body: JSON.stringify({ provider }),});
        const data = await response.json();
        if (!response.ok) {
            alert(data.error || "Unable to unlink account!");
            return;
        }
        alert("Account unlinked successfully!");
        location.reload();
    };
    async function save() {
        const formData = new FormData();
        formData.append("username", profile.username);
        formData.append("bio", profile.bio || "");
        formData.append("private_profile", profile.private_profile ? "true" : "false");
        if (profilePhoto) {
            formData.append("profile_photo", profilePhoto);
        }
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/profiles/personal/`, {method: "PATCH", headers: {Authorization: `Bearer ${localStorage.getItem("access")}`,}, body: formData,});
        const data = await response.json();
        if (!response.ok) {
            setErrors(data);
            return;
        }
        setErrors({});
        alert("Profile edits saved!");
    };
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        const hasPassword = profile.has_password;
        const providers = profile.providers || [];
        return (
            <div className="base-background pl-5 pr-5 pt-10">
                <div className = "grid grid-cols-1 lg:grid-cols-2 gap-10 items-center justify-between">
                    <div className = "space-y-6">
                        <section className = "bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className = "text-3xl font-main-title">Edit Profile</h1></RandomColor>
                            {errors.non_field_errors && (<div className = "text-red-500 text-xl mb-4">{errors.non_field_errors}</div>)}
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title">Username</label>
                                {errors.username && (<p className = "text-red-500 text-xl mt-1">{errors.username}</p>)}
                                <input placeholder = "Username" value = {profile.username} onChange = {(x) => setProfile({...profile, username: x.target.value})} className = "btn w-full mt-3" />
                            </div>
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title">Bio</label>
                                {errors.bio && (<p className = "text-red-500 text-xl mt-1">{errors.bio}</p>)}
                                <textarea placeholder = "Bio" value = {profile.bio} onChange = {(x) => setProfile({...profile, bio: x.target.value})} rows = {4} className = "btn w-full mt-3 min-h-20 max-h-80"></textarea>
                            </div>
                            <label className = "inline-flex items-center space-x-2">
                                <input type="checkbox" checked = {!profile.private_profile} onChange = {() => setProfile({...profile, private_profile: !profile.private_profile})} className = "form-checkbox" />
                                <span>Public Profile</span>
                            </label>
                            <div className = "space-y-2">
                                <label className = "text-xl font-main-title pr-5">Profile Photo</label>
                                {errors.profile_photo && (<p className = "text-red-500 text-xl mt-1">{errors.profile_photo}</p>)}
                                <input type = "file" accept = "image/*" onChange = {(x) => setProfilePhoto(x.target.files?.[0] ?? null)} />
                            </div>
                            <div className = "flex gap-4 mt-4">
                                <RandomColor element = "bg"><button onClick = {save} className = "btn">Save Edits</button></RandomColor>
                                <RandomColor element = "bg"><button onClick = {() => router.push("/profile/")} className = "btn">Cancel Edits</button></RandomColor>
                            </div>
                        </section>
                        {providers.length > 0 && (hasPassword || providers.length > 1) && (
                            <section>
                                <RandomColor constant><h1 className = "text-3xl font-main-title mb-5">Connected Accounts</h1></RandomColor>
                                {providers.map((provider: string) => (
                                    <div key = {provider} className = "flex justify-between items-center">
                                        <button onClick = {() => unlinkAccount(provider)} className = "btn hover:bg-red-500 transition-colors">Unlink {provider} Account</button>
                                    </div>
                                ))}
                            </section>
                        )}
                    </div>
                    <div className = "space-y-6">
                        {hasPassword && <section className = "bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className = "text-xl font-main-title">Change Email</h1></RandomColor>
                            {emailErrors.non_field_errors && (<p className = "text-red-500 text-xl">{emailErrors.non_field_errors[0]}</p>)}
                            {emailErrors.email && (<p className = "text-red-500 text-xl mt-1">{emailErrors.email}</p>)}
                            {emailErrors.current_password && (<p className = "text-red-500 text-xl mt-1">{emailErrors.current_password}</p>)}                            
                            <input type = "email" placeholder = "New Email" value = {profile.email} onChange = {(x) => setProfile({...profile, email: x.target.value})} className = "btn w-full mt-3" />
                            <input type = "password" placeholder = "Current Password" value = {currentPasswordForEmail} onChange = {(x) => setCurrentPasswordForEmail(x.target.value)} className = "btn w-full mt-3" />
                            <RandomColor element = "bg"><button onClick = {emailChange} className = "btn">Change Email</button></RandomColor>
                        </section>}
                        {!hasPassword && (<p className = "text-xl opacity-70">This account uses social login. Set a password to enable password login.</p>)}
                        <section className="bg-ui p-6 rounded-lg shadow-md space-y-4">
                            <RandomColor constant><h1 className="text-xl font-main-title">Change Password</h1></RandomColor>
                            {passwordErrors.non_field_errors && (<p className = "text-red-500 text-xl">{passwordErrors.non_field_errors[0]}</p>)}
                            {passwordErrors.current_password && (<p className = "text-red-500 text-xl mt-1">{passwordErrors.current_password}</p>)}
                            {passwordErrors.confirm_password && (<p className = "text-red-500 text-xl mt-1">{passwordErrors.confirm_password}</p>)}
                            <div className = "grid grid-cols-1 gap-4">
                                {hasPassword && (<input type = "password" placeholder = "Current Password" value = {currentPasswordForPassword} onChange = {(x) => setCurrentPasswordForPassword(x.target.value)} className = "btn w-full" />)}
                                <input type = "password" placeholder = "New Password" value = {newPassword} onChange = {(x) => setNewPassword(x.target.value)} className = "btn w-full" />
                                <input type = "password" placeholder = "Confirm New Password" value = {confirmPassword} onChange = {(x) => setConfirmPassword(x.target.value)} className = "btn w-full" />
                            </div>
                            <RandomColor element = "bg">
                                <button onClick = {passwordChange} className = "btn">Change Password</button>
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