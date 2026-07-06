"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { SectionHeader } from "@/components/section-header";
import { StatCard } from "@/components/stat-card";
import { StatusBadge } from "@/components/status-badge";
import { activeProjects, dashboardStats, recentActivity, ticketColumns } from "@/lib/demo-data";

export default function Dashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const activeTicketCount = ticketColumns.reduce((total, column) => total + column.count, 0);

  useEffect(() => {
    async function verifyAuth() {
      const token = localStorage.getItem("access_token");
      if (!token) {
        router.replace("/login");
        return;
      }
      try {
        const res = await fetch("/api/v1/users/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          throw new Error("Session expired");
        }
      } catch (err: any) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setError(err.message || "Session expired");
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }

    verifyAuth();
  }, [router]);

  if (loading) return <div className="p-6">Loading dashboard…</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Clinic Operations Dashboard"
        description="Monitor project work, patient coordination, and AfterQuery readiness from one workspace."
        action={<StatusBadge tone="success">Day 10 in progress</StatusBadge>}
      />

      <section className="grid gap-4 md:grid-cols-3">
        <a href="/profile" className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm hover:bg-slate-50">
          <h3 className="font-semibold text-slate-950">Profile</h3>
          <p className="mt-1 text-sm text-slate-500">Review your account details and update your profile.</p>
        </a>
        <a href="/projects" className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm hover:bg-slate-50">
          <h3 className="font-semibold text-slate-950">Projects</h3>
          <p className="mt-1 text-sm text-slate-500">Jump into active workstreams and project boards.</p>
        </a>
        <a href="/tickets" className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm hover:bg-slate-50">
          <h3 className="font-semibold text-slate-950">Tickets</h3>
          <p className="mt-1 text-sm text-slate-500">Track patient operations and service requests.</p>
        </a>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {dashboardStats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-950">Project Health</h2>
              <p className="mt-1 text-sm text-slate-500">Active initiatives balanced across clinic and Silver work.</p>
            </div>
            <StatusBadge tone="info">{activeProjects.length} active</StatusBadge>
          </div>

          <div className="mt-5 space-y-4">
            {activeProjects.map((project) => (
              <article key={project.key} className="rounded-lg border border-slate-100 p-4">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <p className="text-sm font-semibold text-slate-950">{project.name}</p>
                    <p className="mt-1 text-xs text-slate-500">
                      {project.key} - {project.owner} - due {project.due}
                    </p>
                  </div>
                  <StatusBadge tone={project.status === "On track" ? "success" : "warning"}>
                    {project.status}
                  </StatusBadge>
                </div>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-sky-600" style={{ width: `${project.progress}%` }} />
                </div>
                <p className="mt-2 text-xs text-slate-500">{project.tickets} tickets tracked</p>
              </article>
            ))}
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-950">Today&apos;s Work</h2>
              <p className="mt-1 text-sm text-slate-500">A compact view of operational momentum.</p>
            </div>
            <StatusBadge tone="neutral">{activeTicketCount} tickets</StatusBadge>
          </div>

          <div className="mt-5 space-y-3">
            {recentActivity.map((activity) => {
              const Icon = activity.icon;
              return (
                <div key={activity.label} className="flex items-center gap-3 rounded-lg bg-slate-50 p-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-white text-sky-700">
                    <Icon className="h-4 w-4" />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-slate-900">{activity.label}</p>
                    <p className="text-xs text-slate-500">{activity.time}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
}
