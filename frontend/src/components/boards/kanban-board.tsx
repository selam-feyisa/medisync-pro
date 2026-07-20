"use client";

import { DndContext, DragEndEvent, DragOverlay, DragStartEvent, PointerSensor, useSensor, useSensors, closestCorners } from "@dnd-kit/core";
import BoardColumn from "./board-column";
import TicketCard from "../tickets/ticket-card";
import { Button } from "@/components/ui/button";
import { Plus, Settings } from "lucide-react";
import { useState } from "react";

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
  onTicketMove?: (ticketId: string, targetColumnId: string) => void;
}

export default function KanbanBoard({ columns, onTicketClick, onAddTicket, onAddColumn, onTicketMove }: KanbanBoardProps) {
  const [activeTicket, setActiveTicket] = useState<Ticket | null>(null);
  
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const ticket = columns.flatMap(col => col.tickets).find(t => t.id === active.id);
    if (ticket) {
      setActiveTicket(ticket);
    }
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveTicket(null);

    if (over && onTicketMove) {
      const ticketId = active.id as string;
      const targetColumnId = over.id as string;
      onTicketMove(ticketId, targetColumnId);
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
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

      <DragOverlay>
        {activeTicket && (
          <div className="rotate-3 opacity-90 shadow-xl">
            <TicketCard {...activeTicket} />
          </div>
        )}
      </DragOverlay>
    </DndContext>
  );
}
