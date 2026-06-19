import Link from 'next/link';

export default function Dashboard() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Welcome back, Dr. Selam</h1>
          <p className="text-gray-600 mt-2">Here's what's happening in your clinic today</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Today</p>
          <p className="text-2xl font-semibold">June 19, 2026</p>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <p className="text-gray-500 text-sm">Today's Appointments</p>
          <p className="text-4xl font-bold mt-2">12</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <p className="text-gray-500 text-sm">Open Tickets</p>
          <p className="text-4xl font-bold mt-2 text-orange-600">8</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <p className="text-gray-500 text-sm">Hours Logged</p>
          <p className="text-4xl font-bold mt-2">6.5h</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <p className="text-gray-500 text-sm">Patients Today</p>
          <p className="text-4xl font-bold mt-2">18</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Tickets</h2>
          <p className="text-gray-500">Ticket management coming soon...</p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            <Link href="/tickets" className="block p-4 bg-blue-50 hover:bg-blue-100 rounded-xl text-center">
              New Ticket
            </Link>
            <Link href="/time-tracking" className="block p-4 bg-teal-50 hover:bg-teal-100 rounded-xl text-center">
              Start Timer
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}