"use client";

import BoardColumn from "./board-column";
import { Button } from "@/components/ui/button";
import { Plus, Settings } from "lucide-react";

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

interface Column {
  id: string;
  name: string;
  tickets: Ticket[];
}

interface KanbanBoardProps {
  columns: Column[];
  onTicketClick?: (ticketId: string) => void;
  onAddTicket?: (columnId: string) => void;
  onAddColumn?: () => void;
}

export default function KanbanBoard({ columns, onTicketClick, onAddTicket, onAddColumn }: KanbanBoardProps) {
  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold text-slate-900">Kanban Board</h2>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4 mr-2" />
            Board Settings
          </Button>
          <Button onClick={onAddColumn} size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Add Column
          </Button>
        </div>
      </div>

      {/* Board */}
      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((column) => (
          <BoardColumn
            key={column.id}
            {...column}
            onTicketClick={onTicketClick}
            onAddTicket={() => onAddTicket?.(column.id)}
          />
        ))}
      </div>
    </div>
  );
}
