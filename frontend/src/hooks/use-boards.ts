import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api-client";

export interface Column {
  id: string;
  name: string;
  position: number;
  tickets: any[];
}

export interface Board {
  id: string;
  name: string;
  project_id: string;
  columns: Column[];
}

export function useBoards(projectId?: string) {
  const [boards, setBoards] = useState<Board[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchBoards() {
      try {
        setLoading(true);
        const endpoint = projectId 
          ? `/projects/${projectId}/boards`
          : "/boards";
        const data = await apiClient.get<Board[]>(endpoint);
        setBoards(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch boards");
      } finally {
        setLoading(false);
      }
    }

    fetchBoards();
  }, [projectId]);

  const createBoard = async (boardData: Partial<Board>) => {
    try {
      const newBoard = await apiClient.post<Board>("/boards", boardData);
      setBoards([...boards, newBoard]);
      return newBoard;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create board");
      throw err;
    }
  };

  const updateBoard = async (id: string, boardData: Partial<Board>) => {
    try {
      const updatedBoard = await apiClient.patch<Board>(`/boards/${id}`, boardData);
      setBoards(boards.map(b => b.id === id ? updatedBoard : b));
      return updatedBoard;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update board");
      throw err;
    }
  };

  const deleteBoard = async (id: string) => {
    try {
      await apiClient.delete(`/boards/${id}`);
      setBoards(boards.filter(b => b.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete board");
      throw err;
    }
  };

  return { boards, loading, error, createBoard, updateBoard, deleteBoard };
}
