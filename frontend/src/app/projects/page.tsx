export default function DocumentsPage() {
  return (
    <div className="max-w-7xl mx-auto px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Documents & Attachments</h1>
        <button className="bg-sky-600 text-white px-6 py-3 rounded-2xl font-medium hover:bg-sky-700 flex items-center gap-2">
          📤 Upload Document
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-3xl p-6 shadow-sm">
          <div className="text-6xl mb-4">📄</div>
          <h3 className="font-semibold">Patient Records</h3>
          <p className="text-gray-500 text-sm mt-1">42 files • 2.3 GB</p>
        </div>
        <div className="bg-white rounded-3xl p-6 shadow-sm">
          <div className="text-6xl mb-4">🖼️</div>
          <h3 className="font-semibold">X-Ray Images</h3>
          <p className="text-gray-500 text-sm mt-1">18 images</p>
        </div>
        <div className="bg-white rounded-3xl p-6 shadow-sm">
          <div className="text-6xl mb-4">📋</div>
          <h3 className="font-semibold">Prescriptions</h3>
          <p className="text-gray-500 text-sm mt-1">31 documents</p>
        </div>
      </div>
    </div>
  );
}