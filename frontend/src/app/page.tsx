'use client';

import Link from 'next/link';

export default function Dashboard() {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 p-6 hidden lg:block">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-9 h-9 bg-sky-600 rounded-xl flex items-center justify-center text-white text-xl">🏥</div>
          <h1 className="text-2xl font-bold text-gray-900">MediSync</h1>
        </div>

        <nav className="space-y-2">
          <Link href="/" className="flex items-center gap-3 px-4 py-3 text-sky-600 bg-sky-50 rounded-xl font-medium">
            📊 Dashboard
          </Link>
          <Link href="/projects" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-100 rounded-xl text-gray-700">
            📁 Projects
          </Link>
          <Link href="/tickets" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-100 rounded-xl text-gray-700">
            🎟️ Tickets
          </Link>
          <Link href="/time-tracking" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-100 rounded-xl text-gray-700">
            ⏱️ Time Tracking
          </Link>
          <Link href="/documents" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-100 rounded-xl text-gray-700">
            📄 Documents
          </Link>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <div className="flex justify-between items-center mb-10">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Good morning, Dr. Selam</h1>
              <p className="text-gray-600 mt-1">Here's an overview of your clinic today</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Friday, June 19 2026</p>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
              <p className="text-gray-500">Today's Appointments</p>
              <p className="text-5xl font-semibold mt-3">14</p>
            </div>
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
              <p className="text-gray-500">Open Tickets</p>
              <p className="text-5xl font-semibold mt-3 text-orange-600">7</p>
            </div>
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
              <p className="text-gray-500">Hours Logged</p>
              <p className="text-5xl font-semibold mt-3">8.5h</p>
            </div>
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
              <p className="text-gray-500">Active Patients</p>
              <p className="text-5xl font-semibold mt-3 text-emerald-600">23</p>
            </div>
          </div>

          <div className="text-center text-gray-400 py-20">
            More pages (Projects, Tickets, Time Tracking, Documents) coming soon...
          </div>
        </div>
      </div>
    </div>
  );
}