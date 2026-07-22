"use client";

import { useState } from "react";
import { Filter, X, ChevronDown } from "lucide-react";

export interface FilterOptions {
  status?: string[];
  priority?: string[];
  assignee?: string[];
  labels?: string[];
}

interface FilterBarProps {
  filters: FilterOptions;
  onFiltersChange: (filters: FilterOptions) => void;
  availableOptions?: {
    statuses: string[];
    priorities: string[];
    assignees: string[];
    labels: string[];
  };
}

export default function FilterBar({ filters, onFiltersChange, availableOptions }: FilterBarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const toggleFilter = (category: keyof FilterOptions, value: string) => {
    const currentFilters = filters[category] || [];
    const newFilters = currentFilters.includes(value)
      ? currentFilters.filter((v) => v !== value)
      : [...currentFilters, value];

    onFiltersChange({
      ...filters,
      [category]: newFilters.length > 0 ? newFilters : undefined,
    });
  };

  const clearFilters = () => {
    onFiltersChange({});
  };

  const hasActiveFilters = Object.values(filters).some((v) => v && v.length > 0);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
          hasActiveFilters
            ? "bg-sky-50 text-sky-700 border border-sky-200"
            : "text-slate-600 hover:bg-slate-100"
        }`}
      >
        <Filter className="w-4 h-4" />
        Filters
        {hasActiveFilters && <span className="w-2 h-2 bg-sky-500 rounded-full"></span>}
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full left-0 mt-2 w-80 bg-white border border-slate-200 rounded-lg shadow-lg z-20">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-slate-200">
              <h3 className="font-medium text-slate-900">Filters</h3>
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="text-xs text-sky-600 hover:text-sky-700"
                >
                  Clear all
                </button>
              )}
            </div>

            {/* Filter sections */}
            <div className="p-4 space-y-4">
              {/* Status */}
              <div>
                <button
                  onClick={() => setActiveSection(activeSection === 'status' ? null : 'status')}
                  className="flex items-center justify-between w-full text-sm font-medium text-slate-900"
                >
                  Status
                  <ChevronDown className={`w-4 h-4 transition-transform ${activeSection === 'status' ? 'rotate-180' : ''}`} />
                </button>
                {activeSection === 'status' && (
                  <div className="mt-2 space-y-2">
                    {availableOptions?.statuses.map((status) => (
                      <label key={status} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.status?.includes(status)}
                          onChange={() => toggleFilter('status', status)}
                          className="rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                        />
                        <span className="text-sm text-slate-700 capitalize">{status}</span>
                      </label>
                    ))}
                  </div>
                )}
              </div>

              {/* Priority */}
              <div>
                <button
                  onClick={() => setActiveSection(activeSection === 'priority' ? null : 'priority')}
                  className="flex items-center justify-between w-full text-sm font-medium text-slate-900"
                >
                  Priority
                  <ChevronDown className={`w-4 h-4 transition-transform ${activeSection === 'priority' ? 'rotate-180' : ''}`} />
                </button>
                {activeSection === 'priority' && (
                  <div className="mt-2 space-y-2">
                    {availableOptions?.priorities.map((priority) => (
                      <label key={priority} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.priority?.includes(priority)}
                          onChange={() => toggleFilter('priority', priority)}
                          className="rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                        />
                        <span className="text-sm text-slate-700 capitalize">{priority}</span>
                      </label>
                    ))}
                  </div>
                )}
              </div>

              {/* Assignee */}
              <div>
                <button
                  onClick={() => setActiveSection(activeSection === 'assignee' ? null : 'assignee')}
                  className="flex items-center justify-between w-full text-sm font-medium text-slate-900"
                >
                  Assignee
                  <ChevronDown className={`w-4 h-4 transition-transform ${activeSection === 'assignee' ? 'rotate-180' : ''}`} />
                </button>
                {activeSection === 'assignee' && (
                  <div className="mt-2 space-y-2">
                    {availableOptions?.assignees.map((assignee) => (
                      <label key={assignee} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.assignee?.includes(assignee)}
                          onChange={() => toggleFilter('assignee', assignee)}
                          className="rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                        />
                        <span className="text-sm text-slate-700">{assignee}</span>
                      </label>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
