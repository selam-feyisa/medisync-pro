"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import { BarChart3, TrendingUp, Clock, Users, CheckCircle, AlertCircle } from "lucide-react";

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("7d");

  const timeRanges = [
    { value: "7d", label: "7 days" },
    { value: "30d", label: "30 days" },
    { value: "90d", label: "90 days" },
    { value: "1y", label: "1 year" },
  ];

  const metrics = {
    totalTickets: 156,
    completedTickets: 89,
    inProgressTickets: 45,
    overdueTickets: 12,
    avgCompletionTime: "3.2 days",
    teamVelocity: 42,
    activeSprints: 3,
    teamMembers: 8,
  };

  const ticketDistribution = [
    { label: "To Do", value: 22, color: "bg-slate-400" },
    { label: "In Progress", value: 45, color: "bg-sky-400" },
    { label: "Done", value: 89, color: "bg-green-400" },
  ];

  const priorityDistribution = [
    { label: "Critical", value: 8, color: "bg-red-500" },
    { label: "High", value: 24, color: "bg-orange-500" },
    { label: "Medium", value: 67, color: "bg-yellow-500" },
    { label: "Low", value: 57, color: "bg-slate-400" },
  ];

  const sprintVelocity = [
    { sprint: "Sprint 1", completed: 35, planned: 40 },
    { sprint: "Sprint 2", completed: 42, planned: 40 },
    { sprint: "Sprint 3", completed: 38, planned: 40 },
    { sprint: "Sprint 4", completed: 45, planned: 40 },
    { sprint: "Sprint 5", completed: 42, planned: 40 },
  ];

  const recentActivity = [
    { id: 1, type: "ticket_completed", message: "Ticket #123 completed", time: "2 hours ago" },
    { id: 2, type: "sprint_started", message: "Sprint 6 started", time: "5 hours ago" },
    { id: 3, type: "member_joined", message: "Alice joined the team", time: "1 day ago" },
    { id: 4, type: "ticket_created", message: "Ticket #124 created", time: "1 day ago" },
    { id: 5, type: "board_updated", message: "Development board updated", time: "2 days ago" },
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case "ticket_completed":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "sprint_started":
        return <TrendingUp className="w-4 h-4 text-sky-600" />;
      case "member_joined":
        return <Users className="w-4 h-4 text-purple-600" />;
      case "ticket_created":
        return <BarChart3 className="w-4 h-4 text-amber-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-slate-600" />;
    }
  };

  return (
    <MainLayout>
      <div className="mx-auto max-w-7xl py-6 px-4">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 flex items-center gap-2">
              <BarChart3 className="w-6 h-6" />
              Analytics Dashboard
            </h1>
            <p className="text-sm text-slate-600 mt-1">
              Track your team's performance and progress
            </p>
          </div>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
          >
            {timeRanges.map((range) => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div>

        {/* Key metrics */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
          <MetricCard
            title="Total Tickets"
            value={metrics.totalTickets}
            icon={<BarChart3 className="w-5 h-5" />}
            trend="+12%"
            trendUp
          />
          <MetricCard
            title="Completed"
            value={metrics.completedTickets}
            icon={<CheckCircle className="w-5 h-5" />}
            trend="+8%"
            trendUp
          />
          <MetricCard
            title="In Progress"
            value={metrics.inProgressTickets}
            icon={<Clock className="w-5 h-5" />}
            trend="-3%"
            trendUp={false}
          />
          <MetricCard
            title="Team Velocity"
            value={metrics.teamVelocity}
            icon={<TrendingUp className="w-5 h-5" />}
            trend="+15%"
            trendUp
          />
        </div>

        {/* Charts row */}
        <div className="grid gap-6 lg:grid-cols-2 mb-6">
          {/* Ticket distribution */}
          <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Ticket Distribution</h3>
            <div className="space-y-4">
              {ticketDistribution.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-600">{item.label}</span>
                    <span className="text-sm font-medium text-slate-900">{item.value}</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div
                      className={`${item.color} h-2 rounded-full transition-all`}
                      style={{ width: `${(item.value / metrics.totalTickets) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Priority distribution */}
          <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Priority Distribution</h3>
            <div className="space-y-4">
              {priorityDistribution.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-600">{item.label}</span>
                    <span className="text-sm font-medium text-slate-900">{item.value}</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div
                      className={`${item.color} h-2 rounded-full transition-all`}
                      style={{ width: `${(item.value / metrics.totalTickets) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sprint velocity chart */}
        <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6 mb-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Sprint Velocity</h3>
          <div className="flex items-end gap-4 h-48">
            {sprintVelocity.map((sprint) => (
              <div key={sprint.sprint} className="flex-1 flex flex-col items-center">
                <div className="w-full flex gap-1 items-end h-32">
                  <div
                    className="flex-1 bg-sky-500 rounded-t transition-all"
                    style={{ height: `${(sprint.completed / sprint.planned) * 100}%` }}
                  />
                  <div className="w-1 bg-slate-200 h-full" />
                </div>
                <div className="mt-2 text-xs text-slate-600 text-center">
                  <p className="font-medium">{sprint.sprint}</p>
                  <p>{sprint.completed}/{sprint.planned}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent activity */}
        <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <div className="flex-shrink-0">{getActivityIcon(activity.type)}</div>
                <div className="flex-1">
                  <p className="text-sm text-slate-900">{activity.message}</p>
                  <p className="text-xs text-slate-500">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

function MetricCard({
  title,
  value,
  icon,
  trend,
  trendUp,
}: {
  title: string;
  value: number;
  icon: React.ReactNode;
  trend: string;
  trendUp: boolean;
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-sky-50 rounded-lg">{icon}</div>
        <span
          className={`text-xs font-medium ${
            trendUp ? "text-green-600" : "text-red-600"
          }`}
        >
          {trend}
        </span>
      </div>
      <p className="text-sm text-slate-600">{title}</p>
      <p className="text-2xl font-semibold text-slate-900 mt-1">{value}</p>
    </div>
  );
}
