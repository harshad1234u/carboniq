import { AlertCircle } from 'lucide-react';
import { Button } from './ui/button';

export function ErrorState({ message, onRetry }: { message: string, onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center bg-red-500/10 rounded-xl border border-red-500/20 p-6">
      <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
      <h3 className="text-lg font-medium text-red-500 mb-2">Something went wrong</h3>
      <p className="text-slate-300 mb-6 max-w-md">{message}</p>
      {onRetry && (
        <Button onClick={onRetry} variant="outline" className="border-red-500/30 text-red-500 hover:bg-red-500/10">
          Try Again
        </Button>
      )}
    </div>
  );
}
