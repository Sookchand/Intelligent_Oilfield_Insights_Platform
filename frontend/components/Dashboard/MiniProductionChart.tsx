'use client';

import { useEffect, useState } from 'react';

interface ProductionData {
  timestamp: string;
  production_rate: number;
}

export default function MiniProductionChart() {
  const [data, setData] = useState<ProductionData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock data for demo - replace with real API call
    const mockData: ProductionData[] = [
      { timestamp: '2024-01-01', production_rate: 950 },
      { timestamp: '2024-01-02', production_rate: 945 },
      { timestamp: '2024-01-03', production_rate: 940 },
      { timestamp: '2024-01-04', production_rate: 920 },
      { timestamp: '2024-01-05', production_rate: 900 },
      { timestamp: '2024-01-06', production_rate: 880 },
      { timestamp: '2024-01-07', production_rate: 850 },
    ];
    setData(mockData);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="h-24 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-halliburton-red"></div>
      </div>
    );
  }

  const maxRate = Math.max(...data.map(d => d.production_rate));
  const minRate = Math.min(...data.map(d => d.production_rate));
  const range = maxRate - minRate;

  // Calculate SVG path
  const width = 300;
  const height = 80;
  const padding = 10;

  const points = data.map((d, i) => {
    const x = (i / (data.length - 1)) * (width - 2 * padding) + padding;
    const y = height - padding - ((d.production_rate - minRate) / range) * (height - 2 * padding);
    return `${x},${y}`;
  });

  const pathData = `M ${points.join(' L ')}`;

  return (
    <div className="relative">
      <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} className="overflow-visible">
        {/* Grid lines */}
        <line
          x1={padding}
          y1={height / 2}
          x2={width - padding}
          y2={height / 2}
          stroke="currentColor"
          strokeWidth="1"
          strokeDasharray="4 4"
          className="text-slate-300 dark:text-slate-600"
        />

        {/* Area fill */}
        <path
          d={`${pathData} L ${width - padding},${height - padding} L ${padding},${height - padding} Z`}
          fill="url(#gradient)"
          opacity="0.2"
        />

        {/* Line */}
        <path
          d={pathData}
          fill="none"
          stroke="#E31837"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Data points */}
        {data.map((d, i) => {
          const x = (i / (data.length - 1)) * (width - 2 * padding) + padding;
          const y = height - padding - ((d.production_rate - minRate) / range) * (height - 2 * padding);
          
          return (
            <circle
              key={i}
              cx={x}
              cy={y}
              r="3"
              fill="#E31837"
              className="hover:r-5 transition-all cursor-pointer"
            >
              <title>{`${d.timestamp}: ${d.production_rate} bbl/day`}</title>
            </circle>
          );
        })}

        {/* Gradient definition */}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#E31837" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#E31837" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>

      {/* Trend indicator */}
      <div className="absolute top-0 right-0 flex items-center space-x-1 text-xs">
        <span className="text-red-600 dark:text-red-400 font-semibold">
          ↓ {((data[data.length - 1].production_rate - data[0].production_rate) / data[0].production_rate * 100).toFixed(1)}%
        </span>
      </div>
    </div>
  );
}

