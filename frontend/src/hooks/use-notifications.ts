import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api-client";

export interface Notification {
  id: string;
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  data?: any;
  action_url?: string;
  created_at: string;
}

export function useNotifications(unreadOnly: boolean = false) {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchNotifications() {
      try {
        setLoading(true);
        const data = await apiClient.get<Notification[]>(
          `/notifications?unread_only=${unreadOnly}`
        );
        setNotifications(data);
        
        // Fetch unread count
        const countData = await apiClient.get<{unread_count: number}>("/notifications/unread/count");
        setUnreadCount(countData.unread_count);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch notifications");
      } finally {
        setLoading(false);
      }
    }

    fetchNotifications();
  }, [unreadOnly]);

  const markAsRead = async (id: string) => {
    try {
      const updated = await apiClient.patch<Notification>(`/notifications/${id}/read`);
      setNotifications(notifications.map(n => n.id === id ? updated : n));
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to mark as read");
      throw err;
    }
  };

  const markAllAsRead = async () => {
    try {
      await apiClient.patch("/notifications/read-all");
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to mark all as read");
      throw err;
    }
  };

  const deleteNotification = async (id: string) => {
    try {
      await apiClient.delete(`/notifications/${id}`);
      setNotifications(notifications.filter(n => n.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete notification");
      throw err;
    }
  };

  return { 
    notifications, 
    unreadCount, 
    loading, 
    error, 
    markAsRead, 
    markAllAsRead, 
    deleteNotification 
  };
}
