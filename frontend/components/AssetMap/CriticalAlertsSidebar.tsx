'use client';

import { useState, useEffect } from 'react';
import { AlertTriangle, TrendingDown, Zap, Droplet, ChevronRight, Sparkles } from 'lucide-react';

interface CriticalAlert {
  id: string;
  assetName: string;
  severity: 'critical' | 'high' | 'medium';
  issue: string;
  productionDrop: number;
  confidence: number;
  reasoning: string;
  timestamp: string;
  location: string;
}

// Mock data - in production, this would come from the SQL Agent
const generateCriticalAlerts = (): CriticalAlert[] => {
  return [
    {
      id: 'alert-1',
      assetName: 'Rig Alpha',
      severity: 'critical',
      issue: 'Production drop >20%',
      productionDrop: -24.5,
      confidence: 0.94,
      reasoning: 'SQL Agent detected 24.5% production decline over 48 hours. Graph Agent identified faulty pressure sensor PS-401. Vector Agent found 3 similar incidents in HSE database.',
      timestamp: '2 hours ago',
      location: 'Permian Basin',
    },
    {
      id: 'alert-2',
      assetName: 'Well PB-1247',
      severity: 'critical',
      issue: 'Sensor fault cascade',
      productionDrop: -18.2,
      confidence: 0.91,
      reasoning: 'Graph Agent detected systemic fault at Substation Alpha affecting 12 wells. SQL shows correlated production drops. Vector search found maintenance delay report.',
      timestamp: '4 hours ago',
      location: 'Permian Basin',
    },
    {
      id: 'alert-3',
      assetName: 'Rig Beta',
      severity: 'high',
      issue: 'Pressure anomaly',
      productionDrop: -15.8,
      confidence: 0.88,
      reasoning: 'SQL Agent flagged abnormal pressure readings. Graph Agent shows no infrastructure issues. Likely localized equipment failure.',
      timestamp: '6 hours ago',
      location: 'Eagle Ford',
    },
    {
      id: 'alert-4',
      assetName: 'Well NS-0089',
      severity: 'high',
      issue: 'Flow rate decline',
      productionDrop: -16.3,
      confidence: 0.85,
      reasoning: 'Gradual decline over 7 days. Vector Agent found similar pattern in historical data. Predicted maintenance window: 48-72 hours.',
      timestamp: '8 hours ago',
      location: 'North Sea',
    },
    {
      id: 'alert-5',
      assetName: 'Rig Gamma',
      severity: 'medium',
      issue: 'Temperature spike',
      productionDrop: -12.1,
      confidence: 0.82,
      reasoning: 'SQL detected temperature anomaly. Graph shows normal dependencies. Vector search suggests seasonal variation.',
      timestamp: '10 hours ago',
      location: 'Bakken',
    },
    {
      id: 'alert-6',
      assetName: 'Well EF-0523',
      severity: 'critical',
      issue: 'Safety alert triggered',
      productionDrop: -22.7,
      confidence: 0.93,
      reasoning: 'HSE system triggered automatic shutdown. Graph Agent confirms isolation successful. Vector Agent found 2 related safety incidents.',
      timestamp: '12 hours ago',
      location: 'Eagle Ford',
    },
    {
      id: 'alert-7',
      assetName: 'Rig Delta',
      severity: 'high',
      issue: 'Power grid instability',
      productionDrop: -17.4,
      confidence: 0.89,
      reasoning: 'Graph Agent detected upstream power issues affecting 8 wells. SQL confirms correlated production drops. External grid fault suspected.',
      timestamp: '14 hours ago',
      location: 'Gulf of Mexico',
    },
    {
      id: 'alert-8',
      assetName: 'Well BK-0312',
      severity: 'medium',
      issue: 'Valve degradation',
      productionDrop: -13.5,
      confidence: 0.80,
      reasoning: 'SQL shows gradual flow reduction. Vector Agent found maintenance schedule overdue by 3 weeks. Preventive action recommended.',
      timestamp: '16 hours ago',
      location: 'Bakken',
    },
    {
      id: 'alert-9',
      assetName: 'Rig Epsilon',
      severity: 'high',
      issue: 'Unexpected shutdown',
      productionDrop: -19.8,
      confidence: 0.90,
      reasoning: 'Emergency shutdown 18 hours ago. Graph Agent shows no infrastructure cause. Vector search found similar incident 6 months ago - equipment failure.',
      timestamp: '18 hours ago',
      location: 'Permian Basin',
    },
    {
      id: 'alert-10',
      assetName: 'Well GM-0156',
      severity: 'medium',
      issue: 'Communication loss',
      productionDrop: -11.2,
      confidence: 0.78,
      reasoning: 'Telemetry gap detected. SQL shows last reading 20 hours ago. Graph Agent confirms network path intact. Likely sensor battery issue.',
      timestamp: '20 hours ago',
      location: 'Gulf of Mexico',
    },
  ];
};

export default function CriticalAlertsSidebar() {
  const [alerts, setAlerts] = useState<CriticalAlert[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<CriticalAlert | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setAlerts(generateCriticalAlerts());
      setLoading(false);
    }, 500);
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-900/30 border-red-600 text-red-400';
      case 'high':
        return 'bg-orange-900/30 border-orange-600 text-orange-400';
      case 'medium':
        return 'bg-yellow-900/30 border-yellow-600 text-yellow-400';
      default:
        return 'bg-slate-900/30 border-slate-600 text-slate-400';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="text-red-500" size={16} />;
      case 'high':
        return <Zap className="text-orange-500" size={16} />;
      default:
        return <Droplet className="text-yellow-500" size={16} />;
    }
  };

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden h-full flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-900/50 to-orange-900/50 border-b border-red-700 p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="text-red-400" size={20} />
            Critical Alerts
          </h3>
          <div className="bg-red-600 text-white text-xs font-bold px-2 py-1 rounded-full animate-pulse">
            {alerts.filter(a => a.severity === 'critical').length}
          </div>
        </div>
        <p className="text-xs text-red-200">
          Top 10 assets requiring immediate attention
        </p>
      </div>

      {/* Alert List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500"></div>
          </div>
        ) : (
          <div className="p-3 space-y-2">
            {alerts.map((alert, index) => (
              <div
                key={alert.id}
                className={`
                  border rounded-lg p-3 cursor-pointer transition-all hover:shadow-lg
                  ${getSeverityColor(alert.severity)}
                  ${selectedAlert?.id === alert.id ? 'ring-2 ring-blue-500' : ''}
                `}
                onClick={() => setSelectedAlert(selectedAlert?.id === alert.id ? null : alert)}
              >
                {/* Alert Header */}
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getSeverityIcon(alert.severity)}
                    <div>
                      <h4 className="font-semibold text-white text-sm">{alert.assetName}</h4>
                      <p className="text-xs text-slate-400">{alert.location}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-bold text-red-400">
                      {alert.productionDrop.toFixed(1)}%
                    </div>
                    <div className="text-[10px] text-slate-500">{alert.timestamp}</div>
                  </div>
                </div>

                {/* Issue */}
                <div className="text-xs text-slate-300 mb-2">{alert.issue}</div>

                {/* Confidence */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    <div className="w-16 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-green-500 to-blue-500"
                        style={{ width: `${alert.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-[10px] text-slate-400">
                      {(alert.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <ChevronRight
                    className={`text-slate-500 transition-transform ${
                      selectedAlert?.id === alert.id ? 'rotate-90' : ''
                    }`}
                    size={14}
                  />
                </div>

                {/* Expanded Reasoning */}
                {selectedAlert?.id === alert.id && (
                  <div className="mt-3 pt-3 border-t border-slate-700">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="text-blue-400" size={14} />
                      <span className="text-xs font-semibold text-blue-400">AI Reasoning Trace</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{alert.reasoning}</p>
                    <button className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold py-2 rounded transition-colors">
                      View Full Analysis
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-slate-800 border-t border-slate-700 p-3">
        <div className="text-xs text-slate-400 text-center">
          Powered by SQL + Graph + Vector Agents
        </div>
      </div>
    </div>
  );
}

