'use client';

import { useState, useMemo, useEffect } from 'react';
import { Database, Network, FileText, Shield, AlertTriangle, TrendingDown } from 'lucide-react';
import { REGIONS } from '@/lib/groundedData';

interface Asset {
  id: string;
  name: string;
  lat: number;
  lng: number;
  status: 'healthy' | 'warning' | 'critical';
  productionRate: number;
  productionTrend: number;
  confidence: number;
  alerts: string[];
  sqlIssues?: string;
  graphIssues?: string;
  vectorIssues?: string;
}

interface Cluster {
  id: string;
  name: string;
  centerLat: number;
  centerLng: number;
  assets: Asset[];
  avgConfidence: number;
  criticalCount: number;
  warningCount: number;
  healthyCount: number;
  avgProductionTrend: number;
}

// Seeded random number generator for consistent SSR/CSR
const seededRandom = (seed: number) => {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};

// Mock data representing thousands of assets across different basins
// GROUNDED IN: frontend/lib/groundedData.ts
const generateMockAssets = (): Asset[] => {
  // Use grounded region data for consistency
  const basins = REGIONS.map(region => ({
    name: region.name,
    lat: region.lat,
    lng: region.lng,
    count: region.totalAssets,
    healthyCount: region.healthyCount,
    warningCount: region.warningCount,
    criticalCount: region.criticalCount,
  }));

  const assets: Asset[] = [];
  let seed = 12345; // Fixed seed for consistency

  basins.forEach((basin, basinIdx) => {
    // Generate exact counts based on grounded data
    let healthyGenerated = 0;
    let warningGenerated = 0;
    let criticalGenerated = 0;

    for (let i = 0; i < basin.count; i++) {
      seed++;
      const rand3 = seededRandom(seed);
      seed++;
      const rand4 = seededRandom(seed);
      seed++;
      const rand5 = seededRandom(seed);
      seed++;
      const rand6 = seededRandom(seed);
      seed++;
      const rand7 = seededRandom(seed);
      seed++;
      const rand8 = seededRandom(seed);

      // Determine status based on grounded counts
      let status: 'healthy' | 'warning' | 'critical';
      if (criticalGenerated < basin.criticalCount) {
        status = 'critical';
        criticalGenerated++;
      } else if (warningGenerated < basin.warningCount) {
        status = 'warning';
        warningGenerated++;
      } else {
        status = 'healthy';
        healthyGenerated++;
      }

      assets.push({
        id: `${basin.name}-${i}`,
        name: `Well ${basin.name.substring(0, 3).toUpperCase()}-${i}`,
        lat: basin.lat + (rand3 - 0.5) * 4,
        lng: basin.lng + (rand4 - 0.5) * 6,
        status,
        productionRate: 800 + rand5 * 200,
        productionTrend: status === 'critical' ? -15 - rand6 * 10 : -5 + rand7 * 10,
        confidence: 0.75 + rand8 * 0.2,
        alerts: status === 'critical' ? ['Production drop', 'Sensor fault'] : [],
        sqlIssues: status === 'critical' ? `${Math.floor(rand5 * 20 + 5)} wells showing <20% flow rate` : undefined,
        graphIssues: status === 'critical' ? 'Shared fault at Substation Alpha' : undefined,
        vectorIssues: status === 'critical' ? '2 matching HSE failure reports' : undefined,
      });
    }
  });

  return assets;
};

export default function AssetClusterMap() {
  const [hoveredCluster, setHoveredCluster] = useState<Cluster | null>(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isMounted, setIsMounted] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  // Only render on client to avoid hydration issues
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const assets = useMemo(() => generateMockAssets(), []);

  // Determine region name based on location
  const getRegionName = (lat: number, lng: number): string => {
    const regions = [
      { name: 'Permian Basin', lat: 32, lng: -102, radius: 5 },
      { name: 'Eagle Ford', lat: 28.5, lng: -98, radius: 5 },
      { name: 'Bakken', lat: 48, lng: -103, radius: 5 },
      { name: 'North Sea', lat: 58, lng: 2, radius: 5 },
      { name: 'Gulf of Mexico', lat: 27, lng: -90, radius: 5 },
    ];

    for (const region of regions) {
      const dist = Math.sqrt(Math.pow(lat - region.lat, 2) + Math.pow(lng - region.lng, 2));
      if (dist < region.radius) {
        return region.name;
      }
    }

    return 'Unknown Region';
  };

  // Cluster assets by geographic proximity
  const clusters = useMemo(() => {
    const clusterRadius = 5 / zoomLevel;
    const clustered: Cluster[] = [];
    const processed = new Set<string>();

    assets.forEach(asset => {
      if (processed.has(asset.id)) return;

      const nearby = assets.filter(a => {
        const dist = Math.sqrt(Math.pow(a.lat - asset.lat, 2) + Math.pow(a.lng - asset.lng, 2));
        return dist < clusterRadius;
      });

      nearby.forEach(a => processed.add(a.id));

      const criticalCount = nearby.filter(a => a.status === 'critical').length;
      const warningCount = nearby.filter(a => a.status === 'warning').length;
      const healthyCount = nearby.filter(a => a.status === 'healthy').length;

      const centerLat = nearby.reduce((sum, a) => sum + a.lat, 0) / nearby.length;
      const centerLng = nearby.reduce((sum, a) => sum + a.lng, 0) / nearby.length;

      clustered.push({
        id: `cluster-${clustered.length}`,
        name: getRegionName(centerLat, centerLng),
        centerLat,
        centerLng,
        assets: nearby,
        avgConfidence: nearby.reduce((sum, a) => sum + a.confidence, 0) / nearby.length,
        criticalCount,
        warningCount,
        healthyCount,
        avgProductionTrend: nearby.reduce((sum, a) => sum + a.productionTrend, 0) / nearby.length,
      });
    });

    return clustered;
  }, [assets, zoomLevel]);

  const getClusterColor = (cluster: Cluster) => {
    if (cluster.criticalCount > cluster.assets.length * 0.15) return '#EF4444'; // Red
    if (cluster.warningCount > cluster.assets.length * 0.2) return '#FF6B35'; // Orange
    return '#10B981'; // Green
  };

  const getClusterSize = (cluster: Cluster) => {
    return Math.min(60, 20 + Math.log(cluster.assets.length) * 8);
  };

  // Convert lat/lng to SVG coordinates
  const project = (lat: number, lng: number) => {
    const x = ((lng + 180) / 360) * 1000;
    const y = ((90 - lat) / 180) * 500;
    return { x, y };
  };

  // Calculate smart tooltip position that stays within bounds
  const getTooltipPosition = (cluster: Cluster) => {
    const pos = project(cluster.centerLat, cluster.centerLng);
    const xPercent = (pos.x / 1000) * 100;
    const yPercent = (pos.y / 500) * 100;

    // Determine horizontal position
    let left = xPercent;
    let translateX = '-50%'; // center by default

    if (xPercent < 25) {
      // Too far left - anchor to left edge with padding
      left = xPercent + 5;
      translateX = '0%';
    } else if (xPercent > 75) {
      // Too far right - anchor to right edge with padding
      left = xPercent - 5;
      translateX = '-100%';
    }

    // Determine vertical position
    let top = yPercent;
    let translateY = 'calc(-100% - 20px)'; // above by default with gap

    if (yPercent < 35) {
      // Too far up - show below with gap
      translateY = '20px';
    } else if (yPercent > 75) {
      // Too far down - show above but closer
      translateY = 'calc(-100% - 10px)';
    }

    return {
      left: `${left}%`,
      top: `${top}%`,
      transform: `translate(${translateX}, ${translateY})`,
      maxWidth: '320px'
    };
  };

  // Show loading state during SSR
  if (!isMounted) {
    return (
      <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
        <div className="bg-slate-800 border-b border-slate-700 p-4">
          <h3 className="text-lg font-semibold text-white">Global Asset Health Map</h3>
          <p className="text-sm text-slate-400 mt-1">Loading asset data...</p>
        </div>
        <div className="h-[500px] flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-halliburton-red"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-700 relative">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700 p-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">Global Asset Health Map</h3>
          <p className="text-sm text-slate-400 mt-1">
            {assets.length.toLocaleString()} assets across {clusters.length} regions
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-xs text-slate-400">Healthy</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="text-xs text-slate-400">Warning</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-xs text-slate-400">Critical</span>
          </div>
        </div>
      </div>

      {/* Map Container */}
      <div className="relative h-[500px] bg-slate-950">
        <svg width="100%" height="100%" viewBox="0 0 1000 500" className="w-full h-full">
          {/* Background grid */}
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#1e293b" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="1000" height="500" fill="url(#grid)" />

          {/* Render clusters */}
          {clusters.map(cluster => {
            const { x, y } = project(cluster.centerLat, cluster.centerLng);
            const size = getClusterSize(cluster);
            const color = getClusterColor(cluster);

            return (
              <g
                key={cluster.id}
                onMouseEnter={() => setHoveredCluster(cluster)}
                onMouseLeave={() => setHoveredCluster(null)}
                className="cursor-pointer transition-all"
              >
                {/* Pulsing ring for critical clusters */}
                {cluster.criticalCount > 0 && (
                  <circle
                    cx={x}
                    cy={y}
                    r={size + 10}
                    fill="none"
                    stroke={color}
                    strokeWidth="2"
                    opacity="0.3"
                    className="animate-ping"
                  />
                )}

                {/* Main cluster circle */}
                <circle
                  cx={x}
                  cy={y}
                  r={size}
                  fill={color}
                  opacity="0.7"
                  stroke="#fff"
                  strokeWidth="2"
                />

                {/* Asset count */}
                <text
                  x={x}
                  y={y}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="text-white font-bold text-sm pointer-events-none"
                  fill="#fff"
                >
                  {cluster.assets.length}
                </text>

                {/* Region name label */}
                <text
                  x={x}
                  y={y + size + 18}
                  textAnchor="middle"
                  className="text-xs pointer-events-none"
                  fill="#94a3b8"
                  fontWeight="600"
                >
                  {cluster.name}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Glass Box Tooltip */}
        {hoveredCluster && (
          <div
            className="absolute bg-slate-800 border-2 border-blue-500 rounded-lg shadow-2xl p-4 w-80 pointer-events-none z-50"
            style={getTooltipPosition(hoveredCluster)}
          >
            {/* Region Name Header */}
            <div className="mb-3 pb-3 border-b border-slate-700">
              <h4 className="font-bold text-white text-lg mb-1">
                {hoveredCluster.name}
              </h4>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400">
                  {hoveredCluster.assets.length} assets
                </span>
                <span className="text-blue-400">
                  {(hoveredCluster.avgConfidence * 100).toFixed(0)}% confidence
                </span>
              </div>
            </div>

            {/* Status breakdown */}
            <div className="grid grid-cols-3 gap-2 mb-3 text-xs">
              <div className="bg-green-900/30 border border-green-600 rounded p-2 text-center">
                <div className="text-green-400 font-bold">{hoveredCluster.healthyCount}</div>
                <div className="text-green-300 text-[10px]">Healthy</div>
              </div>
              <div className="bg-orange-900/30 border border-orange-600 rounded p-2 text-center">
                <div className="text-orange-400 font-bold">{hoveredCluster.warningCount}</div>
                <div className="text-orange-300 text-[10px]">Warning</div>
              </div>
              <div className="bg-red-900/30 border border-red-600 rounded p-2 text-center">
                <div className="text-red-400 font-bold">{hoveredCluster.criticalCount}</div>
                <div className="text-red-300 text-[10px]">Critical</div>
              </div>
            </div>

            {/* Agent Reasoning Trace */}
            <div className="space-y-2 text-[11px] text-slate-300">
              <div className="flex items-start gap-2 bg-slate-900/50 p-2 rounded">
                <Database size={14} className="text-green-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-green-400">SQL Agent:</strong>{' '}
                  {hoveredCluster.criticalCount > 0
                    ? `${hoveredCluster.criticalCount} wells showing production drop >15%`
                    : 'All wells within normal parameters'}
                </div>
              </div>

              <div className="flex items-start gap-2 bg-slate-900/50 p-2 rounded">
                <Network size={14} className="text-purple-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-purple-400">Graph Agent:</strong>{' '}
                  {hoveredCluster.criticalCount > 0
                    ? 'Shared infrastructure fault detected'
                    : 'No systemic dependencies at risk'}
                </div>
              </div>

              <div className="flex items-start gap-2 bg-slate-900/50 p-2 rounded">
                <FileText size={14} className="text-blue-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-blue-400">Vector Agent:</strong>{' '}
                  {hoveredCluster.criticalCount > 0
                    ? `${Math.floor(Math.random() * 5 + 1)} matching HSE reports found`
                    : 'No historical incidents in this region'}
                </div>
              </div>

              <div className="flex items-start gap-2 bg-slate-900/50 p-2 rounded border-t border-slate-700 pt-2 mt-2">
                <Shield size={14} className="text-orange-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-orange-400">Reasoning Agent:</strong>{' '}
                  {(hoveredCluster.avgConfidence * 100).toFixed(0)}% confidence
                  {hoveredCluster.avgProductionTrend < -10 && ' - Grid failure likely'}
                </div>
              </div>
            </div>

            {/* Trend indicator */}
            {hoveredCluster.avgProductionTrend < -10 && (
              <div className="mt-3 bg-red-900/30 border border-red-600 rounded p-2 flex items-center gap-2">
                <TrendingDown className="text-red-400" size={16} />
                <span className="text-xs text-red-300">
                  Avg production trend: {hoveredCluster.avgProductionTrend.toFixed(1)}%
                </span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Zoom controls */}
      <div className="bg-slate-800 border-t border-slate-700 p-3 flex items-center justify-between">
        <div className="text-xs text-slate-400">
          Hover over clusters to see AI reasoning trace
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setZoomLevel(Math.max(0.5, zoomLevel - 0.5))}
            className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white text-xs rounded"
          >
            Zoom Out
          </button>
          <span className="text-xs text-slate-400">{zoomLevel}x</span>
          <button
            onClick={() => setZoomLevel(Math.min(3, zoomLevel + 0.5))}
            className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white text-xs rounded"
          >
            Zoom In
          </button>
        </div>
      </div>
    </div>
  );
}

