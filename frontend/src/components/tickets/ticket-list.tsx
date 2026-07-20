"use client";

import { useState } from "react";
import TicketCard from "./ticket-card";
import { Button } from "@/components/ui/button";
import { Plus, Filter, SortAsc } from "lucide-react";

interface Ticket {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high" | "critical";
  assignee?: string;
  storyPoints?: number;
  commentCount?: number;
  attachmentCount?: number;
}

interface TicketListProps {
  tickets: Ticket[];
  onTicketClick?: (ticketId: string) => void;
  onCreateTicket?: () => void;
}

export default function TicketList({ tickets, onTicketClick, onCreateTicket }: TicketListProps) {
  const [filter, setFilter] = useState<"all" | "todo" | "in_progress" | "done">("all");
  
  const filteredTickets = filter === "all" 
    ? tickets 
    : tickets.filter(t => t.status === filter);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold text-slate-900">Tickets</h2>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </Button>
          <Button variant="outline" size="sm">
            <SortAsc className="w-4 h-4 mr-2" />
            Sort
          </Button>
          <Button onClick={onCreateTicket} size="sm">
            <Plus className="w-4 h-4 mr-2" />
            New Ticket
          </Button>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 mb-6">
        {(["all", "todo", "in_progress", "done"] as const).map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === status
                ? "bg-sky-600 text-white"
                : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1).replace("_", " ")}
          </button>
        ))}
      </div>

      {/* Ticket grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTickets.map((ticket) => (
          <TicketCard
            key={ticket.id}
            {...ticket}
            onClick={() => onTicketClick?.(ticket.id)}
          />
        ))}
      </div>

      {filteredTickets.length === 0 && (
        <div className="text-center py-12">
          <p className="text-slate-500">No tickets found</p>
        </div>
      )}
    </div>
  );
}
