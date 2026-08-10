'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Search, Brain, TrendingUp, Database, Activity, History } from 'lucide-react';

const navItems = [
  { href: '/', label: 'Command Center', icon: Search },
  { href: '/history', label: 'Query History', icon: History },
  { href: '/explainability', label: 'Explainability', icon: Brain },
  { href: '/business', label: 'Business Impact', icon: TrendingUp },
  { href: '/data', label: 'Data Explorer', icon: Database },
  { href: '/system', label: 'System Monitor', icon: Activity },
];

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="bg-white dark:bg-slate-800 shadow-lg border-b border-slate-200 dark:border-slate-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-halliburton-red to-halliburton-red-dark rounded-lg flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">H</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">
                Halliburton <span className="text-halliburton-red">Insights</span>
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Command & Control Center
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-lg transition-all
                    ${isActive
                      ? 'bg-halliburton-red text-white shadow-lg'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 dark:bg-green-900/20 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs font-medium text-green-700 dark:text-green-400">
                System Online
              </span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden flex overflow-x-auto space-x-2 pb-3 -mx-4 px-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center space-x-2 px-3 py-2 rounded-lg whitespace-nowrap transition-all
                  ${isActive
                    ? 'bg-halliburton-red text-white'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                <span className="text-sm font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

