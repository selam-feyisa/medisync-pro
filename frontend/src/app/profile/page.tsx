"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [fullName, setFullName] = useState("");
  const [timezone, setTimezone] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          router.replace("/login");
          return;
        }
        const res = await fetch("/api/v1/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          const j = await res.json();
          throw new Error(j.detail || j.message || "Could not load profile");
        }
        const json = await res.json();
        setProfile(json);
        setFullName(json.full_name || "");
        setTimezone(json.timezone || "UTC");
      } catch (err: any) {
        setError(err.message || "Could not load profile");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  async function handleProfileSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("/api/v1/users/me", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ full_name: fullName, timezone }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail || json.message || "Could not update profile");
      setProfile(json);
      setSuccess("Profile updated successfully");
    } catch (err: any) {
      setError(err.message || "Could not update profile");
    } finally {
      setSaving(false);
    }
  }

  async function handlePasswordChange(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("/api/v1/users/me/password", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail || json.message || "Could not change password");
      setOldPassword("");
      setNewPassword("");
      setSuccess(json.message || "Password updated successfully");
    } catch (err: any) {
      setError(err.message || "Could not change password");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <div className="p-6">Loading profile…</div>;
  if (error && !profile) return <div className="mx-auto max-w-3xl p-6"><div className="rounded-lg bg-red-50 p-4 text-red-600">{error}</div></div>;

  return (
    <div className="mx-auto max-w-3xl py-6 px-4">
      <h1 className="text-2xl font-semibold text-slate-900">Your profile</h1>
      {success && <p className="mt-3 rounded-lg bg-green-50 p-3 text-sm text-green-600">{success}</p>}
      {error && <p className="mt-3 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</p>}

      <div className="mt-6 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Account details</h2>
        <div className="mt-3 space-y-2 text-sm text-slate-600">
          <p><strong>Email:</strong> {profile?.email}</p>
          <p><strong>Status:</strong> {profile?.email_verified ? <span className="text-green-600">Verified</span> : <span className="text-amber-600">Pending verification</span>}</p>
          <p><strong>Timezone:</strong> {profile?.timezone || "UTC"}</p>
        </div>
        {!profile?.email_verified && (
          <div className="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-amber-700">
            Your email is not verified. <a href="/resend-verification" className="text-sky-600 hover:text-sky-700">Resend verification email</a>
          </div>
        )}
      </div>

      <form onSubmit={handleProfileSave} className="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Update profile</h2>
        <div>
          <label className="block text-sm font-medium text-slate-700">Full name</label>
          <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">Timezone</label>
          <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" value={timezone} onChange={(e) => setTimezone(e.target.value)} />
        </div>
        <button disabled={saving} className="rounded-lg bg-sky-600 px-4 py-2 text-white disabled:opacity-60 hover:bg-sky-700 transition-colors">
          {saving ? "Saving…" : "Save profile"}
        </button>
      </form>

      <form onSubmit={handlePasswordChange} className="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Change password</h2>
        <div>
          <label className="block text-sm font-medium text-slate-700">Current password</label>
          <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} type="password" />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">New password</label>
          <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} type="password" />
        </div>
        <button disabled={saving} className="rounded-lg bg-slate-800 px-4 py-2 text-white disabled:opacity-60 hover:bg-slate-900 transition-colors">
          {saving ? "Updating…" : "Change password"}
        </button>
      </form>
    </div>
  );
}
