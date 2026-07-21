"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import { Settings, Bell, Shield, Palette, Globe, Moon, Sun } from "lucide-react";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("notifications");
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const tabs = [
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "security", label: "Security", icon: Shield },
    { id: "appearance", label: "Appearance", icon: Palette },
    { id: "language", label: "Language", icon: Globe },
  ];

  const handleSave = () => {
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      setSuccess("Settings saved successfully");
    }, 1000);
  };

  return (
    <MainLayout>
      <div className="mx-auto max-w-4xl py-6 px-4">
        <h1 className="text-2xl font-semibold text-slate-900 flex items-center gap-2">
          <Settings className="w-6 h-6" />
          Settings
        </h1>

        {success && (
          <div className="mt-4 rounded-lg bg-green-50 p-4 text-sm text-green-700">
            {success}
          </div>
        )}

        <div className="mt-6 flex gap-6">
          {/* Sidebar */}
          <aside className="w-48 flex-shrink-0">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeTab === tab.id
                        ? "bg-sky-50 text-sky-700"
                        : "text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {tab.label}
                  </button>
                );
              })}
            </nav>
          </aside>

          {/* Content */}
          <main className="flex-1">
            {activeTab === "notifications" && (
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Notification Preferences</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-900">Email notifications</p>
                      <p className="text-xs text-slate-500">Receive email updates for your activity</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" defaultChecked className="sr-only peer" />
                      <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-sky-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-600"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-900">Push notifications</p>
                      <p className="text-xs text-slate-500">Receive push notifications in browser</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" defaultChecked className="sr-only peer" />
                      <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-sky-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-600"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-900">Ticket assignments</p>
                      <p className="text-xs text-slate-500">Notify when assigned to a ticket</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" defaultChecked className="sr-only peer" />
                      <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-sky-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-600"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-900">Mentions</p>
                      <p className="text-xs text-slate-500">Notify when mentioned in comments</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" defaultChecked className="sr-only peer" />
                      <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-sky-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-600"></div>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "security" && (
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Security Settings</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-slate-50 rounded-lg">
                    <p className="text-sm font-medium text-slate-900">Two-factor authentication</p>
                    <p className="text-xs text-slate-500 mt-1">Add an extra layer of security to your account</p>
                    <button className="mt-3 px-4 py-2 bg-sky-600 text-white text-sm rounded-lg hover:bg-sky-700 transition-colors">
                      Enable 2FA
                    </button>
                  </div>
                  <div className="p-4 bg-slate-50 rounded-lg">
                    <p className="text-sm font-medium text-slate-900">Active sessions</p>
                    <p className="text-xs text-slate-500 mt-1">Manage your active sessions across devices</p>
                    <button className="mt-3 px-4 py-2 border border-slate-300 text-slate-700 text-sm rounded-lg hover:bg-slate-100 transition-colors">
                      View sessions
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "appearance" && (
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Appearance</h2>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-slate-900 mb-3">Theme</p>
                    <div className="flex gap-3">
                      <button className="flex-1 flex items-center justify-center gap-2 p-4 border-2 border-sky-500 rounded-lg bg-sky-50">
                        <Sun className="w-5 h-5 text-sky-600" />
                        <span className="text-sm font-medium text-sky-700">Light</span>
                      </button>
                      <button className="flex-1 flex items-center justify-center gap-2 p-4 border border-slate-200 rounded-lg hover:border-slate-300 transition-colors">
                        <Moon className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">Dark</span>
                      </button>
                      <button className="flex-1 flex items-center justify-center gap-2 p-4 border border-slate-200 rounded-lg hover:border-slate-300 transition-colors">
                        <Globe className="w-5 h-5 text-slate-600" />
                        <span className="text-sm font-medium text-slate-700">System</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "language" && (
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900 mb-4">Language & Region</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Language</label>
                    <select className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
                      <option>English (US)</option>
                      <option>English (UK)</option>
                      <option>Spanish</option>
                      <option>French</option>
                      <option>German</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Timezone</label>
                    <select className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500">
                      <option>UTC</option>
                      <option>America/New_York</option>
                      <option>America/Los_Angeles</option>
                      <option>Europe/London</option>
                      <option>Europe/Paris</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Save button */}
            <div className="mt-6 flex justify-end">
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-6 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:opacity-60 transition-colors"
              >
                {saving ? "Saving..." : "Save changes"}
              </button>
            </div>
          </main>
        </div>
      </div>
    </MainLayout>
  );
}
