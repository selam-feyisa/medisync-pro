import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api-client";

export interface Ticket {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high" | "critical";
  assignee?: string;
  story_points?: number;
  comment_count?: number;
  attachment_count?: number;
}

export function useTickets(columnId?: string) {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTickets() {
      try {
        setLoading(true);
        const endpoint = columnId 
          ? `/columns/${columnId}/tickets`
          : "/tickets";
        const data = await apiClient.get<Ticket[]>(endpoint);
        setTickets(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch tickets");
      } finally {
        setLoading(false);
      }
    }

    fetchTickets();
  }, [columnId]);

  const createTicket = async (ticketData: Partial<Ticket>) => {
    try {
      const newTicket = await apiClient.post<Ticket>("/tickets", ticketData);
      setTickets([...tickets, newTicket]);
      return newTicket;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create ticket");
      throw err;
    }
  };

  const updateTicket = async (id: string, ticketData: Partial<Ticket>) => {
    try {
      const updatedTicket = await apiClient.patch<Ticket>(`/tickets/${id}`, ticketData);
      setTickets(tickets.map(t => t.id === id ? updatedTicket : t));
      return updatedTicket;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update ticket");
      throw err;
    }
  };

  const deleteTicket = async (id: string) => {
    try {
      await apiClient.delete(`/tickets/${id}`);
      setTickets(tickets.filter(t => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete ticket");
      throw err;
    }
  };

  return { tickets, loading, error, createTicket, updateTicket, deleteTicket };
}
