"use client";

import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token") || "";
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/v1/auth/password-reset/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: password }),
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.detail || j.message || "Reset failed");
      setMessage(j.message || "Password reset successfully");
      setTimeout(() => router.push('/login'), 1200);
    } catch (err: any) {
      setError(err.message || "Reset failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md py-12 px-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-2xl font-semibold text-slate-900">Reset password</h1>
        <p className="mb-6 text-sm text-slate-600">Enter your new password below.</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">New password</label>
          <input className="mt-1 w-full rounded-lg border px-3 py-2" value={password} onChange={(e)=>setPassword(e.target.value)} type="password" required />
        </div>
        {error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        {message && <div className="rounded-lg bg-green-50 p-3 text-sm text-green-600">{message}</div>}
        <div>
          <button disabled={loading} className="w-full rounded-lg bg-sky-600 px-4 py-2 text-white disabled:opacity-60">{loading? 'Resetting...':'Reset password'}</button>
        </div>
      </form>
      <p className="mt-4 text-sm text-slate-600">Remember your password? <a href="/login" className="text-sky-600 hover:text-sky-700">Sign in</a></p>
      </div>
    </div>
  );
}
