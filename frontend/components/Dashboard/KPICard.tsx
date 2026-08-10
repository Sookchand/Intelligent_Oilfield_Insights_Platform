'use client';

import { ReactNode } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  icon: ReactNode;
  color: 'red' | 'blue' | 'green' | 'orange' | 'gray';
  subtitle?: string;
}

const colorClasses = {
  red: {
    bg: 'from-red-500 to-red-600',
    text: 'text-red-600',
    light: 'bg-red-50 dark:bg-red-900/20',
  },
  blue: {
    bg: 'from-blue-500 to-blue-600',
    text: 'text-blue-600',
    light: 'bg-blue-50 dark:bg-blue-900/20',
  },
  green: {
    bg: 'from-green-500 to-green-600',
    text: 'text-green-600',
    light: 'bg-green-50 dark:bg-green-900/20',
  },
  orange: {
    bg: 'from-orange-500 to-orange-600',
    text: 'text-orange-600',
    light: 'bg-orange-50 dark:bg-orange-900/20',
  },
  gray: {
    bg: 'from-gray-500 to-gray-600',
    text: 'text-gray-600',
    light: 'bg-gray-50 dark:bg-gray-900/20',
  },
};

export default function KPICard({
  title,
  value,
  unit,
  trend,
  trendValue,
  icon,
  color,
  subtitle,
}: KPICardProps) {
  const colors = colorClasses[color];

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4" />;
      case 'down':
        return <TrendingDown className="w-4 h-4" />;
      case 'stable':
        return <Minus className="w-4 h-4" />;
      default:
        return null;
    }
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-green-600 dark:text-green-400';
    if (trend === 'down') return 'text-red-600 dark:text-red-400';
    return 'text-gray-600 dark:text-gray-400';
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden hover:shadow-xl transition-shadow">
      {/* Header with Icon */}
      <div className={`bg-gradient-to-r ${colors.bg} p-4`}>
        <div className="flex items-center justify-between">
          <div className="text-white">
            <p className="text-sm font-medium opacity-90">{title}</p>
            <div className="flex items-baseline space-x-2 mt-1">
              <span className="text-3xl font-bold">{value}</span>
              {unit && <span className="text-lg opacity-75">{unit}</span>}
            </div>
          </div>
          <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
            {icon}
          </div>
        </div>
      </div>

      {/* Body with Trend */}
      <div className="p-4">
        {trend && trendValue && (
          <div className={`flex items-center space-x-2 ${getTrendColor()}`}>
            {getTrendIcon()}
            <span className="text-sm font-semibold">{trendValue}</span>
            <span className="text-xs text-slate-500 dark:text-slate-400">vs last week</span>
          </div>
        )}
        {subtitle && (
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}

