"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Ticket, 
  FolderKanban, 
  Calendar, 
  BarChart3, 
  Settings,
  Bell,
  Users
} from "lucide-react";

const navItems = [
  { href: "/", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/tickets", icon: Ticket, label: "Tickets" },
  { href: "/boards", icon: FolderKanban, label: "Boards" },
  { href: "/sprints", icon: Calendar, label: "Sprints" },
  { href: "/analytics", icon: BarChart3, label: "Analytics" },
  { href: "/notifications", icon: Bell, label: "Notifications" },
  { href: "/team", icon: Users, label: "Team" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-200 bg-white h-screen fixed left-0 top-0">
      <div className="p-6 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900">DevFlow Pro</h1>
      </div>
      
      <nav className="p-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-sky-50 text-sky-700"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
