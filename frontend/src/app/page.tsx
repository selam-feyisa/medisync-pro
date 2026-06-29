import { SectionHeader } from "@/components/section-header";
import { StatCard } from "@/components/stat-card";
import { StatusBadge } from "@/components/status-badge";
import { activeProjects, dashboardStats, recentActivity, ticketColumns } from "@/lib/demo-data";

export default function Dashboard() {
  const activeTicketCount = ticketColumns.reduce((total, column) => total + column.count, 0);

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Clinic Operations Dashboard"
        description="Monitor project work, patient coordination, and AfterQuery readiness from one workspace."
        action={<StatusBadge tone="success">Day 10 in progress</StatusBadge>}
      />

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
