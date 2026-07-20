"use client";

import { useState } from "react";
import { MoreHorizontal, Plus } from "lucide-react";
import TicketCard from "../tickets/ticket-card";

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

interface BoardColumnProps {
  id: string;
  name: string;
  tickets: Ticket[];
  onTicketClick?: (ticketId: string) => void;
  onAddTicket?: () => void;
}

export default function BoardColumn({ id, name, tickets, onTicketClick, onAddTicket }: BoardColumnProps) {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="flex-shrink-0 w-80 bg-slate-100 rounded-lg p-4">
      {/* Column header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="font-medium text-slate-900">{name}</h3>
          <span className="bg-slate-200 text-slate-600 text-xs px-2 py-0.5 rounded-full">
            {tickets.length}
          </span>
        </div>
        <button className="p-1 hover:bg-slate-200 rounded transition-colors">
          <MoreHorizontal className="w-4 h-4 text-slate-500" />
        </button>
      </div>

      {/* Tickets */}
      <div className="space-y-3 min-h-[200px]">
        {tickets.map((ticket) => (
          <TicketCard
            key={ticket.id}
            {...ticket}
            onClick={() => onTicketClick?.(ticket.id)}
          />
        ))}
      </div>

      {/* Add ticket button */}
      <button
        onClick={onAddTicket}
        className="mt-4 w-full flex items-center justify-center gap-2 p-2 text-sm text-slate-600 hover:bg-slate-200 rounded-lg transition-colors"
      >
        <Plus className="w-4 h-4" />
        Add ticket
      </button>
    </div>
  );
}
