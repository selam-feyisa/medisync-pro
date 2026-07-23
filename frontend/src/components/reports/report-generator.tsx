"use client";

import { useState } from "react";
import { FileText, Download, Calendar, Filter, Check } from "lucide-react";

interface ReportConfig {
  type: "tickets" | "sprints" | "team" | "time";
  dateRange: "7d" | "30d" | "90d" | "custom";
  startDate?: string;
  endDate?: string;
  format: "pdf" | "csv" | "xlsx";
}

interface ReportGeneratorProps {
  onGenerate?: (config: ReportConfig) => void;
}

export default function ReportGenerator({ onGenerate }: ReportGeneratorProps) {
  const [config, setConfig] = useState<ReportConfig>({
    type: "tickets",
    dateRange: "30d",
    format: "pdf",
  });
  const [isGenerating, setIsGenerating] = useState(false);

  const reportTypes = [
    { value: "tickets", label: "Ticket Report", description: "Summary of all tickets" },
    { value: "sprints", label: "Sprint Report", description: "Sprint performance metrics" },
    { value: "team", label: "Team Report", description: "Team productivity analysis" },
    { value: "time", label: "Time Tracking Report", description: "Time spent on tasks" },
  ];

  const dateRanges = [
    { value: "7d", label: "Last 7 days" },
    { value: "30d", label: "Last 30 days" },
    { value: "90d", label: "Last 90 days" },
    { value: "custom", label: "Custom range" },
  ];

  const formats = [
    { value: "pdf", label: "PDF" },
    { value: "csv", label: "CSV" },
    { value: "xlsx", label: "Excel" },
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulate report generation
    await new Promise((resolve) => setTimeout(resolve, 2000));
    onGenerate?.(config);
    setIsGenerating(false);
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
      <div className="flex items-center gap-2 mb-6">
        <FileText className="w-5 h-5 text-slate-600" />
        <h2 className="text-lg font-semibold text-slate-900">Generate Report</h2>
      </div>

      <div className="space-y-6">
        {/* Report type */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-3">Report Type</label>
          <div className="grid gap-3 md:grid-cols-2">
            {reportTypes.map((type) => (
              <button
                key={type.value}
                onClick={() => setConfig({ ...config, type: type.value as any })}
                className={`p-4 border-2 rounded-lg text-left transition-colors ${
                  config.type === type.value
                    ? "border-sky-500 bg-sky-50"
                    : "border-slate-200 hover:border-slate-300"
                }`}
              >
                <div className="flex items-center gap-2">
                  {config.type === type.value && (
                    <Check className="w-4 h-4 text-sky-600" />
                  )}
                  <span className="font-medium text-slate-900">{type.label}</span>
                </div>
                <p className="text-sm text-slate-500 mt-1">{type.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Date range */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Date Range
          </label>
          <div className="flex gap-2">
            {dateRanges.map((range) => (
              <button
                key={range.value}
                onClick={() => setConfig({ ...config, dateRange: range.value as any })}
                className={`px-4 py-2 rounded-lg border-2 text-sm font-medium transition-colors ${
                  config.dateRange === range.value
                    ? "border-sky-500 bg-sky-50 text-sky-700"
                    : "border-slate-200 text-slate-600 hover:border-slate-300"
                }`}
              >
                {range.label}
              </button>
            ))}
          </div>

          {config.dateRange === "custom" && (
            <div className="mt-3 grid gap-3 md:grid-cols-2">
              <div>
                <label className="block text-xs text-slate-600 mb-1">Start Date</label>
                <input
                  type="date"
                  value={config.startDate || ""}
                  onChange={(e) => setConfig({ ...config, startDate: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-600 mb-1">End Date</label>
                <input
                  type="date"
                  value={config.endDate || ""}
                  onChange={(e) => setConfig({ ...config, endDate: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm"
                />
              </div>
            </div>
          )}
        </div>

        {/* Format */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-3">Export Format</label>
          <div className="flex gap-2">
            {formats.map((format) => (
              <button
                key={format.value}
                onClick={() => setConfig({ ...config, format: format.value as any })}
                className={`px-4 py-2 rounded-lg border-2 text-sm font-medium transition-colors ${
                  config.format === format.value
                    ? "border-sky-500 bg-sky-50 text-sky-700"
                    : "border-slate-200 text-slate-600 hover:border-slate-300"
                }`}
              >
                {format.label}
              </button>
            ))}
          </div>
        </div>

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isGenerating ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              Generate Report
            </>
          )}
        </button>
      </div>
    </div>
  );
}
