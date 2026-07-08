"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showResendVerification, setShowResendVerification] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.detail || json.message || "Login failed");
      // store tokens
      localStorage.setItem("access_token", json.access_token);
      localStorage.setItem("refresh_token", json.refresh_token);
      router.push("/");
    } catch (err: any) {
      const message = err.message || "Login failed";
      setError(message);
      setShowResendVerification(message.toLowerCase().includes("not verified"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md py-12 px-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-2xl font-semibold text-slate-900">Sign in to your account</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Email</label>
          <input
            className="mt-1 w-full rounded-lg border px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Password</label>
          <input
            className="mt-1 w-full rounded-lg border px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
          />
        </div>

        {error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        {showResendVerification && (
          <p className="text-sm text-slate-600">
            Need a new verification email?{' '}
            <a href="/resend-verification" className="text-sky-600">
              Resend verification
            </a>
          </p>
        )}

        <div>
          <button
            disabled={loading}
            className="w-full rounded-lg bg-sky-600 px-4 py-2 text-white disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </div>
      </form>

      <div className="mt-4 space-y-2 text-sm text-slate-600">
        <div className="flex justify-between">
          <a href="/forgot-password" className="text-sky-600 hover:text-sky-700">Forgot password?</a>
          <a href="/resend-verification" className="text-sky-600 hover:text-sky-700">Resend verification</a>
        </div>
        <p>Don't have an account? <a href="/register" className="text-sky-600 hover:text-sky-700">Register</a></p>
      </div>
      </div>
    </div>
  );
}
