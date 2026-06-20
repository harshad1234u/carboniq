import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { NAV_ITEMS } from '../utils/constants';
import { Leaf, LogOut } from 'lucide-react';
import { Button } from './ui/button';
import { cn } from '../lib/utils';

export function Layout({ children }: { children: React.ReactNode }) {
  const { signOut } = useAuth();
  const location = useLocation();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col md:flex-row">
      {/* Desktop Sidebar */}
      <aside role="navigation" aria-label="Main navigation" className="hidden md:flex flex-col w-64 border-r border-slate-800 bg-slate-900/50 backdrop-blur-sm p-4 sticky top-0 h-screen">
        <div className="flex items-center gap-2 mb-8 px-2">
          <Leaf className="w-6 h-6 text-emerald-500" />
          <span className="text-xl font-bold tracking-tight">CarbonIQ</span>
        </div>
        
        <nav className="flex-1 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname.startsWith(item.path);
            return (
              <Link
                key={item.path}
                to={item.path}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors",
                  isActive 
                    ? "bg-emerald-500/10 text-emerald-500" 
                    : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/50"
                )}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto pt-4 border-t border-slate-800">
          <Button 
            variant="ghost" 
            className="w-full justify-start text-slate-400 hover:text-slate-100" 
            onClick={signOut}
          >
            <LogOut className="w-5 h-5 mr-3" />
            Sign Out
          </Button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main role="main" aria-label="Page content" className="flex-1 flex flex-col min-w-0 pb-16 md:pb-0 overflow-y-auto min-h-screen">
        {/* Mobile Header */}
        <header className="md:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-20">
          <div className="flex items-center gap-2">
            <Leaf className="w-5 h-5 text-emerald-500" />
            <span className="font-bold">CarbonIQ</span>
          </div>
          <Button variant="ghost" size="sm" onClick={signOut}>
            <LogOut className="w-4 h-4" />
          </Button>
        </header>
        
        <div className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
          {children}
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <nav role="navigation" aria-label="Mobile navigation" className="md:hidden fixed bottom-0 left-0 right-0 border-t border-slate-800 bg-slate-900/90 backdrop-blur-md z-20 pb-safe">
        <div className="flex justify-around items-center p-2">
          {NAV_ITEMS.slice(0, 5).map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname.startsWith(item.path);
            return (
              <Link
                key={item.path}
                to={item.path}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex flex-col items-center justify-center p-2 min-w-[64px] transition-colors",
                  isActive ? "text-emerald-500" : "text-slate-400"
                )}
              >
                <Icon className="w-5 h-5 mb-1" />
                <span className="text-[10px] font-medium truncate">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
