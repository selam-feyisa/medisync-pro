"use client";

import { Ticket, Clock, User, MessageSquare, Paperclip } from "lucide-react";
import { StatusBadge } from "../status-badge";

interface TicketCardProps {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high" | "critical";
  assignee?: string;
  storyPoints?: number;
  commentCount?: number;
  attachmentCount?: number;
  onClick?: () => void;
}

export default function TicketCard({
  id,
  title,
  description,
  status,
  priority,
  assignee,
  storyPoints,
  commentCount = 0,
  attachmentCount = 0,
  onClick,
}: TicketCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-white border border-slate-200 rounded-lg p-4 hover:border-sky-300 hover:shadow-sm transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <Ticket className="w-4 h-4 text-slate-400" />
          <span className="text-xs text-slate-500">#{id.slice(0, 8)}</span>
        </div>
        <StatusBadge status={status} />
      </div>

      <h3 className="font-medium text-slate-900 mb-1">{title}</h3>
      <p className="text-sm text-slate-600 mb-3 line-clamp-2">{description}</p>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {assignee && (
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <User className="w-3 h-3" />
              <span>{assignee}</span>
            </div>
          )}
          {storyPoints && (
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <Clock className="w-3 h-3" />
              <span>{storyPoints} pts</span>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          {commentCount > 0 && (
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <MessageSquare className="w-3 h-3" />
              <span>{commentCount}</span>
            </div>
          )}
          {attachmentCount > 0 && (
            <div className="flex items-center gap-1 text-xs text-slate-500">
              <Paperclip className="w-3 h-3" />
              <span>{attachmentCount}</span>
            </div>
          )}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100">
        <span
          className={`inline-block px-2 py-1 rounded text-xs font-medium ${
            priority === "critical"
              ? "bg-red-100 text-red-700"
              : priority === "high"
              ? "bg-orange-100 text-orange-700"
              : priority === "medium"
              ? "bg-yellow-100 text-yellow-700"
              : "bg-slate-100 text-slate-700"
          }`}
        >
          {priority.charAt(0).toUpperCase() + priority.slice(1)}
        </span>
      </div>
    </div>
  );
}
