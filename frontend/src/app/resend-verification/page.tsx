"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function ResendVerificationPage() {
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
      const res = await fetch('/api/v1/auth/resend-verification', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.detail || j.message || 'Request failed');
      setMessage('If an account exists, a verification email was sent');
      setTimeout(() => router.push('/login'), 2000);
    } catch (err: any) {
      setError(err.message || 'Request failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md py-12">
      <h1 className="mb-4 text-2xl font-semibold">Resend verification</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Email</label>
          <input className="mt-1 w-full rounded-lg border px-3 py-2" value={email} onChange={(e)=>setEmail(e.target.value)} type="email" required />
        </div>
        {error && <div className="text-red-600">{error}</div>}
        {message && <div className="text-green-600">{message}</div>}
        <div>
          <button disabled={loading} className="w-full rounded-lg bg-sky-600 px-4 py-2 text-white disabled:opacity-60">{loading? 'Sending...':'Resend verification email'}</button>
        </div>
      </form>
    </div>
  );
}
