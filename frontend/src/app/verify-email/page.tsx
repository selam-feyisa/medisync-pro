"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function VerifyEmailPage() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token") || "";
  const [status, setStatus] = useState<string>("pending");
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    async function verify() {
      try {
        const res = await fetch("/api/v1/auth/verify-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token }),
        });
        const j = await res.json();
        if (!res.ok) throw new Error(j.detail || j.message || "Verification failed");
        setStatus("success");
        setMessage(j.message || "Email verified. You can now sign in.");
        setTimeout(() => router.push('/login'), 1500);
      } catch (err: any) {
        setStatus("error");
        setMessage(err.message || "Verification failed");
      }
    }
    if (token) verify();
    else { setStatus("error"); setMessage("Missing token"); }
  }, [token]);

  return (
    <div className="mx-auto max-w-md py-12 px-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-2xl font-semibold text-slate-900">Email verification</h1>
        <div>
          {status === 'pending' && <p className="text-slate-600">Verifying your email...</p>}
          {status === 'success' && <p className="rounded-lg bg-green-50 p-4 text-green-600">{message}</p>}
          {status === 'error' && <p className="rounded-lg bg-red-50 p-4 text-red-600">{message}</p>}
        </div>
        {status === 'error' && (
          <p className="mt-4 text-sm text-slate-600">
            Need a new verification link? <a href="/resend-verification" className="text-sky-600 hover:text-sky-700">Resend verification</a>
          </p>
        )}
      </div>
    </div>
  );
}
