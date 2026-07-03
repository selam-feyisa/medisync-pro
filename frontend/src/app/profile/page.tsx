"use client";

import { useEffect, useState } from "react";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch("/api/v1/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          const j = await res.json();
          throw new Error(j.detail || j.message || "Could not load profile");
        }
        const json = await res.json();
        setProfile(json);
      } catch (err: any) {
        setError(err.message || "Could not load profile");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div>Loading profile...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return (
    <div className="mx-auto max-w-md py-6">
      <h1 className="text-2xl font-semibold">Your profile</h1>
      <div className="mt-4 space-y-2">
        <div><strong>Full name:</strong> {profile.full_name}</div>
        <div><strong>Email:</strong> {profile.email} {profile.email_verified ? <span className="text-xs text-green-600">(verified)</span> : <span className="text-xs text-yellow-600">(unverified)</span>}</div>
        <div><strong>Timezone:</strong> {profile.timezone}</div>
      </div>
    </div>
  );
}
