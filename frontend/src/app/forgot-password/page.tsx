"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/v1/auth/password-reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.detail || j.message || 'Request failed');
      setMessage('If an account exists, a reset email was sent');
      setTimeout(() => router.push('/login'), 2000);
    } catch (err: any) {
      setError(err.message || 'Request failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md py-12 px-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-2xl font-semibold text-slate-900">Forgot password</h1>
        <p className="mb-6 text-sm text-slate-600">Enter your email address and we'll send you a link to reset your password.</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Email</label>
          <input className="mt-1 w-full rounded-lg border px-3 py-2" value={email} onChange={(e)=>setEmail(e.target.value)} type="email" required />
        </div>
        {error && <div className="text-red-600">{error}</div>}
        {message && <div className="text-green-600">{message}</div>}
        <div>
          <button disabled={loading} className="w-full rounded-lg bg-sky-600 px-4 py-2 text-white disabled:opacity-60">{loading? 'Sending...':'Send reset email'}</button>
        </div>
      </form>
      <p className="mt-4 text-sm text-slate-600">Remember your password? <a href="/login" className="text-sky-600 hover:text-sky-700">Sign in</a></p>
      </div>
    </div>
  );
}
