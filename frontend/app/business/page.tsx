'use client';

import { TrendingUp } from 'lucide-react';

export default function BusinessPage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12 text-center">
        <TrendingUp className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          Business Impact Analytics
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Coming soon - Downtime costs, ROI analysis, safety risk scoring, and production forecasting
        </p>
      </div>
    </div>
  );
}

