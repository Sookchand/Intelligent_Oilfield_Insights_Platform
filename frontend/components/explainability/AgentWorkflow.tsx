'use client';

import { ReasoningStep } from '@/lib/api';
import { FileSearch, Database, Network, Brain, CheckCircle, Clock, Lightbulb } from 'lucide-react';

interface AgentWorkflowProps {
  reasoningTrace: ReasoningStep[];
}

const agentIcons: Record<string, any> = {
  'Parser': FileSearch,
  'SQL': Database,
  'Graph': Network,
  'Ontology': Lightbulb,
  'Reasoning': Brain,
};

const agentColors: Record<string, string> = {
  'Parser': 'from-blue-500 to-blue-600',
  'SQL': 'from-green-500 to-green-600',
  'Graph': 'from-purple-500 to-purple-600',
  'Ontology': 'from-amber-500 to-orange-600',
  'Reasoning': 'from-orange-500 to-orange-600',
};

export default function AgentWorkflow({ reasoningTrace }: AgentWorkflowProps) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">
        Agent Workflow Visualization
      </h2>

      <div className="relative">
        {/* Workflow Steps */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {reasoningTrace.map((step, idx) => {
            const Icon = agentIcons[step.agent] || Brain;
            const colorClass = agentColors[step.agent] || 'from-gray-500 to-gray-600';

            return (
              <div key={idx} className="relative">
                {/* Agent Card */}
                <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4 border-2 border-slate-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-500 transition-all">
                  {/* Step Number */}
                  <div className="absolute -top-3 -left-3 w-8 h-8 bg-white dark:bg-slate-800 border-2 border-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
                      {step.step}
                    </span>
                  </div>

                  {/* Agent Icon */}
                  <div className={`w-12 h-12 bg-gradient-to-br ${colorClass} rounded-lg flex items-center justify-center mb-3`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  {/* Agent Name */}
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-1">
                    {step.agent} Agent
                  </h3>

                  {/* Action */}
                  <p className="text-xs text-slate-600 dark:text-slate-400 mb-3">
                    {step.action}
                  </p>

                  {/* Duration */}
                  {step.duration_ms && (
                    <div className="flex items-center space-x-1 text-xs text-slate-500 dark:text-slate-500">
                      <Clock className="w-3 h-3" />
                      <span>{step.duration_ms.toFixed(0)}ms</span>
                    </div>
                  )}

                  {/* Status */}
                  <div className="mt-2 flex items-center space-x-1">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-xs text-green-600 dark:text-green-400 font-medium">
                      Complete
                    </span>
                  </div>
                </div>

                {/* Arrow to next step */}
                {idx < reasoningTrace.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-2 transform -translate-y-1/2 z-10">
                    <div className="w-4 h-4 bg-blue-500 rotate-45 transform translate-x-1"></div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Total Processing Time */}
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <span className="font-semibold text-blue-900 dark:text-blue-300">
                Total Processing Time
              </span>
            </div>
            <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {reasoningTrace.reduce((sum, step) => sum + (step.duration_ms || 0), 0).toFixed(0)}ms
            </span>
          </div>
        </div>

        {/* Workflow Summary */}
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Agents Used</p>
            <p className="text-xl font-bold text-slate-900 dark:text-white">
              {new Set(reasoningTrace.map(s => s.agent)).size}
            </p>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Total Steps</p>
            <p className="text-xl font-bold text-slate-900 dark:text-white">
              {reasoningTrace.length}
            </p>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Databases Queried</p>
            <p className="text-xl font-bold text-slate-900 dark:text-white">
              {reasoningTrace.filter(s => s.sql_query || s.cypher_query).length}
            </p>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Avg Step Time</p>
            <p className="text-xl font-bold text-slate-900 dark:text-white">
              {(reasoningTrace.reduce((sum, step) => sum + (step.duration_ms || 0), 0) / reasoningTrace.length).toFixed(0)}ms
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

