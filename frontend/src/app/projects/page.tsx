export default function ProjectsPage() {
  return (
    <div className="max-w-7xl mx-auto px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <button className="bg-sky-600 text-white px-5 py-2.5 rounded-xl font-medium hover:bg-sky-700">
          + New Project
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-3xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
            <div className="h-2 bg-sky-500 rounded-full w-3/4 mb-6"></div>
            <h3 className="font-semibold text-xl">Clinic Management System</h3>
            <p className="text-gray-500 mt-1">Q2 2026 • 12 tickets</p>
            
            <div className="mt-8 flex gap-2">
              <div className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">In Progress</div>
              <div className="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">3 members</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}