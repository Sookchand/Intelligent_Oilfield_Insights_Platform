'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { queryAPI, QueryResponse } from '@/lib/api';
import QueryInput from '@/components/QueryInput';
import ResultsDisplay from '@/components/ResultsDisplay';
import DemoQueries from '@/components/DemoQueries';
import DatabaseHealthMatrix from '@/components/Dashboard/DatabaseHealthMatrix';
import KPICard from '@/components/Dashboard/KPICard';
import MiniProductionChart from '@/components/Dashboard/MiniProductionChart';
import AssetClusterMap from '@/components/AssetMap/AssetClusterMap';
import CriticalAlertsSidebar from '@/components/AssetMap/CriticalAlertsSidebar';
import { Sparkles, Droplet, Shield, Activity, TrendingDown, Map } from 'lucide-react';
import { GLOBAL_KPIS } from '@/lib/groundedData';

export default function HomePage() {
  const [currentQuery, setCurrentQuery] = useState('');
  const [queryResult, setQueryResult] = useState<QueryResponse | null>(null);
  const [conversationHistory, setConversationHistory] = useState<Array<{ query: string, answer: string }>>([]);

  const queryMutation = useMutation({
    mutationFn: (query: string) => queryAPI.processQuery(query),
    onSuccess: (data) => {
      setQueryResult(data);
      // Add to conversation history
      setConversationHistory(prev => [...prev, {
        query: currentQuery,
        answer: data.answer
      }]);
    },
  });

  const handleQuery = (query: string) => {
    setCurrentQuery(query);
    queryMutation.mutate(query);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-3 py-8">
        <div className="flex items-center justify-center space-x-3">
          <Sparkles className="w-8 h-8 text-halliburton-red" />
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white">
            Oilfield Intelligence Platform
          </h1>
        </div>
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          AI-powered analytics for production optimization and asset management
        </p>
      </div>

      {/* KPI Dashboard - Only show when no query is active */}
      {!queryResult && !queryMutation.isPending && (
        <>
          {/* Database Health Matrix */}
          <DatabaseHealthMatrix />

          {/* KPI Cards - Grounded in GLOBAL_KPIS */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <KPICard
              title="Production Rate"
              value={GLOBAL_KPIS.avgProductionRate.toFixed(1)}
              unit="bbl/day"
              trend="down"
              trendValue={`${GLOBAL_KPIS.productionTrend}%`}
              icon={<Droplet className="w-6 h-6 text-white" />}
              color="red"
              subtitle="Average across all active rigs"
            />
            <KPICard
              title="Asset Health"
              value={Math.round(GLOBAL_KPIS.assetHealthPercentage).toString()}
              unit="%"
              trend="stable"
              trendValue={`+${GLOBAL_KPIS.assetHealthTrend}%`}
              icon={<Activity className="w-6 h-6 text-white" />}
              color="green"
              subtitle="Equipment operational status"
            />
            <KPICard
              title="Safety Alerts"
              value={GLOBAL_KPIS.criticalAlertsCount.toString()}
              unit="unread"
              trend="up"
              trendValue={`+${GLOBAL_KPIS.safetyAlertsTrend}`}
              icon={<Shield className="w-6 h-6 text-white" />}
              color="orange"
              subtitle="HSE reports requiring attention"
            />
          </div>

          {/* Geospatial Asset Map + Critical Alerts */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Asset Cluster Map - Takes 2 columns */}
            <div className="lg:col-span-2">
              <AssetClusterMap />
            </div>

            {/* Critical Alerts Sidebar - Takes 1 column */}
            <div className="lg:col-span-1">
              <CriticalAlertsSidebar />
            </div>
          </div>

          {/* Production Trend Card */}
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Production Trend (Last 7 Days)
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                  Rig Alpha showing declining output
                </p>
              </div>
              <div className="flex items-center space-x-2 text-red-600 dark:text-red-400">
                <TrendingDown className="w-5 h-5" />
                <span className="text-sm font-semibold">Declining</span>
              </div>
            </div>
            <MiniProductionChart />
          </div>
        </>
      )}

      {/* Demo Queries */}
      <DemoQueries onSelectQuery={handleQuery} />

      {/* Query Input - Prominent Search Bar */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-halliburton-red/20 via-transparent to-halliburton-red/20 rounded-xl blur-xl"></div>
        <div className="relative">
          <QueryInput
            onSubmit={handleQuery}
            isLoading={queryMutation.isPending}
          />
        </div>
      </div>

      {/* Results */}
      {queryMutation.isPending && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
          <div className="flex items-center justify-center space-x-3">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="text-slate-600 dark:text-slate-400">
              Processing your query through multi-agent system...
            </p>
          </div>
        </div>
      )}

      {queryMutation.isError && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6">
          <h3 className="text-red-800 dark:text-red-400 font-semibold mb-2">
            Error Processing Query
          </h3>
          <p className="text-red-600 dark:text-red-300">
            {queryMutation.error instanceof Error ? queryMutation.error.message : 'An error occurred'}
          </p>
        </div>
      )}

      {queryResult && !queryMutation.isPending && (
        <ResultsDisplay
          query={currentQuery}
          result={queryResult}
        />
      )}

      {/* Footer Info */}
      {!queryResult && !queryMutation.isPending && (
        <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-6 border border-slate-200 dark:border-slate-700">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <p className="text-2xl font-bold text-halliburton-red mb-1">5 Agents</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Parser • SQL • Graph • Ontology • Reasoning
              </p>
            </div>
            <div>
              <p className="text-2xl font-bold text-halliburton-blue mb-1">4 Databases</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                PostgreSQL • Neo4j • Qdrant • MinIO
              </p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600 mb-1">100% Transparent</p>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Full reasoning trace & audit trail
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

