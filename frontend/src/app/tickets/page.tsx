"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import TicketList from "@/components/tickets/ticket-list";

export default function TicketsPage() {
  const [tickets] = useState([
    {
      id: "1",
      title: "Implement user authentication",
      description: "Add OAuth2 login with Google and GitHub providers",
      status: "in_progress" as const,
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
    {
      id: "3",
      title: "Setup database schema",
      description: "Define PostgreSQL tables and relationships",
      status: "done" as const,
      priority: "critical" as const,
      assignee: "Bob Johnson",
      storyPoints: 8,
      commentCount: 5,
      attachmentCount: 0,
    },
  ]);

  const handleTicketClick = (ticketId: string) => {
    console.log("Clicked ticket:", ticketId);
  };

  const handleCreateTicket = () => {
    console.log("Create new ticket");
  };

  return (
    <MainLayout>
      <TicketList
        tickets={tickets}
        onTicketClick={handleTicketClick}
        onCreateTicket={handleCreateTicket}
      />
    </MainLayout>
  );
}
