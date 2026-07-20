"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import KanbanBoard from "@/components/boards/kanban-board";

export default function BoardsPage() {
  const [columns] = useState([
    {
      id: "1",
      name: "To Do",
      tickets: [
        {
          id: "1",
          title: "Implement user authentication",
          description: "Add OAuth2 login with Google and GitHub providers",
          status: "todo" as const,
          priority: "high" as const,
          assignee: "John Doe",
          storyPoints: 5,
          commentCount: 3,
          attachmentCount: 1,
        },
        {
          id: "2",
          title: "Design dashboard UI",
          description: "Create wireframes and mockups for the main dashboard",
          status: "todo" as const,
          priority: "medium" as const,
          assignee: "Jane Smith",
          storyPoints: 3,
          commentCount: 0,
          attachmentCount: 2,
        },
      ],
    },
    {
      id: "2",
      name: "In Progress",
      tickets: [
        {
          id: "3",
          title: "Setup database schema",
          description: "Define PostgreSQL tables and relationships",
          status: "in_progress" as const,
          priority: "critical" as const,
          assignee: "Bob Johnson",
          storyPoints: 8,
          commentCount: 5,
          attachmentCount: 0,
        },
      ],
    },
    {
      id: "3",
      name: "Done",
      tickets: [
        {
          id: "4",
          title: "Initialize project",
          description: "Set up Next.js and FastAPI project structure",
          status: "done" as const,
          priority: "low" as const,
          assignee: "Alice Brown",
          storyPoints: 2,
          commentCount: 1,
          attachmentCount: 0,
        },
      ],
    },
  ]);

  const handleTicketClick = (ticketId: string) => {
    console.log("Clicked ticket:", ticketId);
  };

  const handleAddTicket = (columnId: string) => {
    console.log("Add ticket to column:", columnId);
  };

  const handleAddColumn = () => {
    console.log("Add new column");
  };

  return (
    <MainLayout>
      <KanbanBoard
        columns={columns}
        onTicketClick={handleTicketClick}
        onAddTicket={handleAddTicket}
        onAddColumn={handleAddColumn}
      />
    </MainLayout>
  );
}
