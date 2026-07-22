"use client";

import { useState } from "react";
import { ArrowUpDown, ChevronDown } from "lucide-react";

export type SortOption = "created_at" | "updated_at" | "priority" | "title" | "assignee";
export type SortDirection = "asc" | "desc";

interface SortBarProps {
  sortBy: SortOption;
  sortDirection: SortDirection;
  onSortChange: (sortBy: SortOption, sortDirection: SortDirection) => void;
}

const sortOptions: { value: SortOption; label: string }[] = [
  { value: "created_at", label: "Created date" },
  { value: "updated_at", label: "Updated date" },
  { value: "priority", label: "Priority" },
  { value: "title", label: "Title" },
  { value: "assignee", label: "Assignee" },
];

export default function SortBar({ sortBy, sortDirection, onSortChange }: SortBarProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleSortChange = (value: SortOption) => {
    if (sortBy === value) {
      // Toggle direction if same option
      onSortChange(value, sortDirection === "asc" ? "desc" : "asc");
    } else {
      // New option, default to desc
      onSortChange(value, "desc");
    }
    setIsOpen(false);
  };

  const currentLabel = sortOptions.find((opt) => opt.value === sortBy)?.label || "Sort";

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition-colors"
      >
        <ArrowUpDown className="w-4 h-4" />
        {currentLabel}
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full left-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg shadow-lg z-20">
            <div className="py-2">
              {sortOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleSortChange(option.value)}
                  className={`w-full px-4 py-2 text-left text-sm transition-colors ${
                    sortBy === option.value
                      ? "bg-sky-50 text-sky-700"
                      : "text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>{option.label}</span>
                    {sortBy === option.value && (
                      <span className="text-xs text-slate-500">
                        {sortDirection === "asc" ? "↑" : "↓"}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
