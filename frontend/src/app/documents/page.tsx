import { FileUp, FolderOpen } from "lucide-react";
import { SectionHeader } from "@/components/section-header";
import { StatusBadge } from "@/components/status-badge";
import { documents } from "@/lib/demo-data";

export default function DocumentsPage() {
  const totalFiles = documents.reduce((total, document) => total + document.files, 0);

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-6">
      <SectionHeader
        title="Documents"
        description="Manage patient files, ticket attachments, and AfterQuery review evidence."
        action={
          <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-sky-600 px-3 text-sm font-medium text-white hover:bg-sky-700">
            <FileUp className="h-4 w-4" />
            Upload
          </button>
        }
      />

      <section className="grid gap-4 md:grid-cols-3">
        <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-500">Total files</p>
          <p className="mt-3 text-3xl font-semibold text-slate-950">{totalFiles}</p>
        </article>
        <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-500">Storage tracked</p>
          <p className="mt-3 text-3xl font-semibold text-slate-950">3.34 GB</p>
        </article>
        <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-500">Upload status</p>
          <p className="mt-3 text-3xl font-semibold text-emerald-700">Ready</p>
        </article>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        {documents.map((document) => (
          <article key={document.name} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start gap-4">
              <span className="flex h-11 w-11 items-center justify-center rounded-lg bg-slate-100 text-sky-700">
                <FolderOpen className="h-5 w-5" />
              </span>
              <div className="min-w-0 flex-1">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                  <h2 className="font-semibold text-slate-950">{document.name}</h2>
                  <StatusBadge tone="info">{document.type}</StatusBadge>
                </div>
                <p className="mt-2 text-sm text-slate-500">
                  {document.files} files · {document.size}
                </p>
              </div>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}
