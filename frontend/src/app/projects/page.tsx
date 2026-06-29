import { Plus, SlidersHorizontal } from "lucide-react";
import { SectionHeader } from "@/components/section-header";
import { StatusBadge } from "@/components/status-badge";
import { activeProjects } from "@/lib/demo-data";

export default function ProjectsPage() {
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Projects"
        description="Track clinic initiatives, implementation work, and AfterQuery preparation tasks."
        action={
          <>
            <button className="inline-flex h-10 items-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-medium text-slate-700 hover:bg-slate-100">
              <SlidersHorizontal className="h-4 w-4" />
              Filters
            </button>
            <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-sky-600 px-3 text-sm font-medium text-white hover:bg-sky-700">
              <Plus className="h-4 w-4" />
              Project
            </button>
          </>
        }
      />

      <section className="grid gap-4 lg:grid-cols-3">
        {activeProjects.map((project) => (
          <article key={project.key} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-normal text-sky-700">{project.key}</p>
                <h2 className="mt-2 text-lg font-semibold text-slate-950">{project.name}</h2>
              </div>
              <StatusBadge tone={project.status === "On track" ? "success" : "warning"}>{project.status}</StatusBadge>
            </div>

            <div className="mt-6 space-y-3 text-sm text-slate-600">
              <div className="flex justify-between">
                <span>Owner</span>
                <span className="font-medium text-slate-950">{project.owner}</span>
              </div>
              <div className="flex justify-between">
                <span>Due</span>
                <span className="font-medium text-slate-950">{project.due}</span>
              </div>
              <div className="flex justify-between">
                <span>Tickets</span>
                <span className="font-medium text-slate-950">{project.tickets}</span>
              </div>
            </div>

            <div className="mt-6">
              <div className="mb-2 flex justify-between text-xs text-slate-500">
                <span>Progress</span>
                <span>{project.progress}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-sky-600" style={{ width: `${project.progress}%` }} />
              </div>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}
