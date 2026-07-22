"use client";

import { useState } from "react";
import { Bell, Search, User } from "lucide-react";
import SearchBar from "@/components/search/search-bar";
import NotificationPanel from "@/components/notifications/notification-panel";

export default function Header() {
  const [showSearch, setShowSearch] = useState(false);

  return (
    <header className="h-16 border-b border-slate-200 bg-white fixed left-64 right-0 top-0 z-10">
      <div className="h-full px-6 flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-md">
          {showSearch ? (
            <div>
              <SearchBar onResultClick={(result) => console.log("Navigating to:", result)} />
              <button
                onClick={() => setShowSearch(false)}
                className="mt-2 text-sm text-slate-600 hover:text-slate-900"
              >
                Cancel
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowSearch(true)}
              className="flex items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition-colors w-full"
            >
              <Search className="w-4 h-4" />
              Search tickets...
            </button>
          )}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <NotificationPanel />

          {/* User menu */}
          <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
            <div className="text-right">
              <p className="text-sm font-medium text-slate-900">John Doe</p>
              <p className="text-xs text-slate-500">Admin</p>
            </div>
            <div className="w-8 h-8 bg-sky-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
              JD
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
