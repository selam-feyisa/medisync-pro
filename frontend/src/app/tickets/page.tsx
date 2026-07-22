"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import TicketList from "@/components/tickets/ticket-list";
import FilterBar, { FilterOptions } from "@/components/filters/filter-bar";
import SortBar, { SortOption, SortDirection } from "@/components/filters/sort-bar";

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

  const [filters, setFilters] = useState<FilterOptions>({});
  const [sortBy, setSortBy] = useState<SortOption>("created_at");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const handleTicketClick = (ticketId: string) => {
    console.log("Clicked ticket:", ticketId);
  };

  const handleCreateTicket = () => {
    console.log("Create new ticket");
  };

  const availableOptions = {
    statuses: ["todo", "in_progress", "done"],
    priorities: ["low", "medium", "high", "critical"],
    assignees: ["John Doe", "Jane Smith", "Bob Johnson"],
    labels: ["bug", "feature", "improvement"],
  };

  return (
    <MainLayout>
      <div className="mb-4 flex items-center gap-3">
        <FilterBar
          filters={filters}
          onFiltersChange={setFilters}
          availableOptions={availableOptions}
        />
        <SortBar
          sortBy={sortBy}
          sortDirection={sortDirection}
          onSortChange={(newSortBy, newSortDirection) => {
            setSortBy(newSortBy);
            setSortDirection(newSortDirection);
          }}
        />
      </div>
      <TicketList
        tickets={tickets}
        onTicketClick={handleTicketClick}
        onCreateTicket={handleCreateTicket}
      />
    </MainLayout>
  );
}
