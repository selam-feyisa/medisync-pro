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
    <div className="mx-auto max-w-md py-12">
      <h1 className="mb-4 text-2xl font-semibold">Email verification</h1>
      <div>
        {status === 'pending' && <p>Verifying...</p>}
        {status === 'success' && <p className="text-green-600">{message}</p>}
        {status === 'error' && <p className="text-red-600">{message}</p>}
      </div>
    </div>
  );
}
