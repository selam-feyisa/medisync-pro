"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import ReportGenerator from "@/components/reports/report-generator";
import { FileText, Download, Trash2, Calendar } from "lucide-react";

interface GeneratedReport {
  id: string;
  name: string;
  type: string;
  format: string;
  generatedAt: string;
  size: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<GeneratedReport[]>([
    {
      id: "1",
      name: "Ticket Report - July 2024",
      type: "tickets",
      format: "pdf",
      generatedAt: "2024-07-15",
      size: "2.4 MB",
    },
    {
      id: "2",
      name: "Sprint Report - Q2 2024",
      type: "sprints",
      format: "xlsx",
      generatedAt: "2024-06-30",
      size: "1.8 MB",
    },
    {
      id: "3",
      name: "Team Productivity - June 2024",
      type: "team",
      format: "pdf",
      generatedAt: "2024-06-15",
      size: "3.1 MB",
    },
  ]);

  const handleGenerateReport = (config: any) => {
    const newReport: GeneratedReport = {
      id: Date.now().toString(),
      name: `${config.type.charAt(0).toUpperCase() + config.type.slice(1)} Report - ${new Date().toLocaleDateString()}`,
      type: config.type,
      format: config.format,
      generatedAt: new Date().toISOString().split("T")[0],
      size: "1.5 MB",
    };
    setReports([newReport, ...reports]);
  };

  const handleDownload = (reportId: string) => {
    console.log("Downloading report:", reportId);
  };

  const handleDelete = (reportId: string) => {
    setReports(reports.filter((r) => r.id !== reportId));
  };

  const getFormatBadge = (format: string) => {
    switch (format) {
      case "pdf":
        return "bg-red-100 text-red-700";
      case "csv":
        return "bg-green-100 text-green-700";
      case "xlsx":
        return "bg-blue-100 text-blue-700";
      default:
        return "bg-slate-100 text-slate-700";
    }
  };

  return (
    <MainLayout>
      <div className="mx-auto max-w-6xl py-6 px-4">
        <div className="flex items-center gap-2 mb-6">
          <FileText className="w-6 h-6" />
          <h1 className="text-2xl font-semibold text-slate-900">Reports</h1>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Report generator */}
          <div className="lg:col-span-1">
            <ReportGenerator onGenerate={handleGenerateReport} />
          </div>

          {/* Generated reports */}
          <div className="lg:col-span-2">
            <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-slate-900">Generated Reports</h2>
                <span className="text-sm text-slate-500">{reports.length} reports</span>
              </div>

              {reports.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                  <p className="text-slate-500">No reports generated yet</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {reports.map((report) => (
                    <div
                      key={report.id}
                      className="flex items-center justify-between p-4 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="p-2 bg-slate-100 rounded-lg">
                          <FileText className="w-5 h-5 text-slate-600" />
                        </div>
                        <div>
                          <p className="font-medium text-slate-900">{report.name}</p>
                          <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
                            <span className="flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              {report.generatedAt}
                            </span>
                            <span>•</span>
                            <span>{report.size}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium uppercase ${getFormatBadge(
                            report.format
                          )}`}
                        >
                          {report.format}
                        </span>
                        <button
                          onClick={() => handleDownload(report.id)}
                          className="p-2 text-slate-600 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors"
                          title="Download"
                        >
                          <Download className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(report.id)}
                          className="p-2 text-slate-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
