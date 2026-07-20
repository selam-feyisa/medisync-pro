interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({ message = "Loading..." }: LoadingStateProps) {
  return (
    <div className="flex items-center justify-center min-h-[200px]">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-sky-600"></div>
        <p className="mt-3 text-sm text-slate-600">{message}</p>
      </div>
    </div>
  );
}

export function InlineLoading({ size = "sm" }: { size?: "sm" | "md" }) {
  const sizeClasses = size === "sm" ? "h-4 w-4" : "h-6 w-6";
  return (
    <div className={`inline-block animate-spin rounded-full ${sizeClasses} border-b-2 border-sky-600`}></div>
  );
}

export function SkeletonCard() {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 animate-pulse">
      <div className="flex items-center justify-between mb-2">
        <div className="h-4 w-20 bg-slate-200 rounded"></div>
        <div className="h-4 w-16 bg-slate-200 rounded"></div>
      </div>
      <div className="h-5 w-full bg-slate-200 rounded mb-2"></div>
      <div className="h-4 w-3/4 bg-slate-200 rounded mb-3"></div>
      <div className="flex items-center justify-between">
        <div className="h-4 w-24 bg-slate-200 rounded"></div>
        <div className="h-4 w-16 bg-slate-200 rounded"></div>
      </div>
    </div>
  );
}
