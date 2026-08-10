'use client';

import { TrendingDown, AlertTriangle, BarChart3, Zap } from 'lucide-react';

interface DemoQueriesProps {
  onSelectQuery: (query: string) => void;
}

const demoQueries = [
  {
    icon: TrendingDown,
    query: "Why is production dropping at Rig Alpha?",
    description: "Analyze production trends and identify issues",
    color: "from-red-500 to-orange-500"
  },
  {
    icon: AlertTriangle,
    query: "Show me all faulty equipment at Rig Alpha",
    description: "Find equipment failures and relationships",
    color: "from-yellow-500 to-amber-500"
  },
  {
    icon: BarChart3,
    query: "What is the safety risk at Well W-12?",
    description: "Calculate safety risk scores",
    color: "from-purple-500 to-pink-500"
  },
  {
    icon: Zap,
    query: "Predict production for next week",
    description: "Forecast future production trends",
    color: "from-blue-500 to-cyan-500"
  },
];

export default function DemoQueries({ onSelectQuery }: DemoQueriesProps) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          Try These Demo Queries
        </h2>
        <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-xs font-medium rounded-full">
          Demo Mode
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {demoQueries.map((demo, idx) => {
          const Icon = demo.icon;
          
          return (
            <button
              key={idx}
              onClick={() => onSelectQuery(demo.query)}
              className="group relative overflow-hidden bg-slate-50 dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 rounded-lg p-4 text-left transition-all hover:shadow-lg"
            >
              <div className="flex items-start space-x-3">
                <div className={`p-2 bg-gradient-to-br ${demo.color} rounded-lg`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-900 dark:text-white mb-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {demo.query}
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {demo.description}
                  </p>
                </div>
              </div>

              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

