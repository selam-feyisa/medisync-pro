export default function TimeTrackingPage() {
  return (
    <div className="max-w-7xl mx-auto px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Time Tracking</h1>
        <button className="bg-emerald-600 text-white px-6 py-3 rounded-2xl font-medium hover:bg-emerald-700 flex items-center gap-2">
          ⏱️ Start New Timer
        </button>
      </div>

      <div className="bg-white rounded-3xl shadow-sm p-8 text-center">
        <div className="text-7xl mb-6">⏱️</div>
        <h2 className="text-2xl font-semibold mb-3">No Active Timer</h2>
        <p className="text-gray-500 mb-8">Start tracking time on a ticket</p>
        
        <button className="bg-emerald-600 text-white px-10 py-4 rounded-2xl text-lg font-medium hover:bg-emerald-700">
          Start Timer
        </button>
      </div>

      <div className="mt-12">
        <h3 className="text-xl font-semibold mb-4">Recent Entries</h3>
        <p className="text-gray-500">Recent time entries will appear here...</p>
      </div>
    </div>
  );
}