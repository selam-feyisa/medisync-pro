import { Pause, Play, Plus } from "lucide-react";
import { SectionHeader } from "@/components/section-header";
import { StatusBadge } from "@/components/status-badge";
import { timeEntries } from "@/lib/demo-data";

export default function TimeTrackingPage() {
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Time Tracking"
        description="Track ticket work, submit entries, and review approval status."
        action={
          <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-emerald-600 px-3 text-sm font-medium text-white hover:bg-emerald-700">
            <Plus className="h-4 w-4" />
            Manual Entry
          </button>
        }
      />

      <section className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
        <article className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">Active timer</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-950">MS-124 Dashboard metrics polish</h2>
            </div>
            <StatusBadge tone="success">Running</StatusBadge>
          </div>

          <p className="mt-8 text-5xl font-semibold tracking-normal text-slate-950">01:24:18</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-slate-950 px-4 text-sm font-medium text-white hover:bg-slate-800">
              <Pause className="h-4 w-4" />
              Pause
            </button>
            <button className="inline-flex h-10 items-center gap-2 rounded-lg border border-slate-200 px-4 text-sm font-medium text-slate-700 hover:bg-slate-100">
              <Play className="h-4 w-4" />
              Switch Ticket
            </button>
          </div>
        </article>

        <article className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-slate-500">Weekly summary</p>
          <p className="mt-3 text-4xl font-semibold text-slate-950">32.5h</p>
          <div className="mt-6 space-y-3 text-sm text-slate-600">
            <div className="flex justify-between"><span>Billable</span><span className="font-medium text-slate-950">24.8h</span></div>
            <div className="flex justify-between"><span>Pending approval</span><span className="font-medium text-slate-950">5.4h</span></div>
            <div className="flex justify-between"><span>Approved</span><span className="font-medium text-slate-950">19.4h</span></div>
          </div>
        </article>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-5 py-4">
          <h2 className="text-lg font-semibold text-slate-950">Recent Entries</h2>
        </div>
        <div className="divide-y divide-slate-100">
          {timeEntries.map((entry) => (
            <div key={`${entry.ticket}-${entry.task}`} className="grid gap-3 px-5 py-4 text-sm md:grid-cols-[120px_1fr_120px_120px] md:items-center">
              <span className="font-medium text-sky-700">{entry.ticket}</span>
              <span className="text-slate-900">{entry.task}</span>
              <span className="text-slate-600">{entry.duration}</span>
              <StatusBadge tone={entry.status === "Approved" ? "success" : entry.status === "Draft" ? "warning" : "info"}>
                {entry.status}
              </StatusBadge>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
