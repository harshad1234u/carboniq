import { cn } from "../lib/utils"

export function LoadingSkeleton({ variant = 'default' }: { variant?: 'default' | 'card' | 'chart' | 'dashboard' | 'text' }) {
  if (variant === 'dashboard') {
    return (
      <div className="space-y-8 w-full animate-pulse">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-64 bg-slate-800/50 rounded-xl"></div>
          <div className="h-64 bg-slate-800/50 rounded-xl"></div>
        </div>
        <div className="h-40 bg-slate-800/50 rounded-xl"></div>
        <div className="h-64 bg-slate-800/50 rounded-xl"></div>
      </div>
    );
  }

  if (variant === 'card') {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 shadow-sm animate-pulse">
        <div className="h-6 w-1/3 bg-slate-800 rounded mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 w-full bg-slate-800 rounded"></div>
          <div className="h-4 w-5/6 bg-slate-800 rounded"></div>
          <div className="h-4 w-4/6 bg-slate-800 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("animate-pulse bg-slate-800/50 rounded-md", variant === 'text' ? 'h-4 w-full' : 'h-32 w-full')}></div>
  );
}
