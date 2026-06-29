import { Plus, Search } from "lucide-react";
import { SectionHeader } from "@/components/section-header";
import { StatusBadge } from "@/components/status-badge";
import { ticketColumns } from "@/lib/demo-data";

export default function TicketsPage() {
  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Tickets"
        description="Review work across backlog, active delivery, clinical review, and completed items."
        action={
          <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-sky-600 px-3 text-sm font-medium text-white hover:bg-sky-700">
            <Plus className="h-4 w-4" />
            Ticket
          </button>
        }
      />

      <div className="relative max-w-xl">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          className="h-10 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm outline-none transition focus:border-sky-500"
          placeholder="Search by ticket, assignee, or clinical workflow"
        />
      </div>

      <section className="grid gap-4 xl:grid-cols-4">
        {ticketColumns.map((column) => (
          <div key={column.title} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="font-semibold text-slate-950">{column.title}</h2>
              <StatusBadge tone="neutral">{column.count}</StatusBadge>
            </div>

            <div className="space-y-3">
              {column.tickets.map((ticket) => (
                <article key={ticket.id} className="rounded-lg border border-slate-100 bg-slate-50 p-3">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-semibold text-sky-700">{ticket.id}</span>
                    <StatusBadge tone={ticket.priority === "High" ? "danger" : ticket.priority === "Medium" ? "warning" : "neutral"}>
                      {ticket.priority}
                    </StatusBadge>
                  </div>
                  <h3 className="mt-3 text-sm font-medium leading-5 text-slate-950">{ticket.title}</h3>
                  <p className="mt-3 text-xs text-slate-500">Assigned to {ticket.assignee}</p>
                </article>
              ))}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
