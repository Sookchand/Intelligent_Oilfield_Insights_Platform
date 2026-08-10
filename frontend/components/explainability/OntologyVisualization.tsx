'use client';

import { ReasoningStep } from '@/lib/api';
import { Lightbulb, ArrowRight, BookOpen } from 'lucide-react';

interface OntologyVisualizationProps {
  reasoningTrace: ReasoningStep[];
}

export default function OntologyVisualization({ reasoningTrace }: OntologyVisualizationProps) {
  // Find ontology reasoning step
  const ontologyStep = reasoningTrace.find(step => step.agent === 'Ontology');

  if (!ontologyStep || !ontologyStep.causal_explanation) {
    return null;
  }

  // Debug logging
  console.log('Ontology Step:', ontologyStep);
  console.log('Details:', ontologyStep.details);
  console.log('Confidence:', ontologyStep.details?.confidence);

  const confidence = ontologyStep.details?.confidence || 0;
  const ruleName = ontologyStep.details?.rule_name || 'Unknown Rule';
  const ruleId = ontologyStep.details?.rule_id || '';

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 border-2 border-amber-200 dark:border-amber-700">
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-amber-100 dark:bg-amber-900/40 rounded-lg">
          <Lightbulb className="w-6 h-6 text-amber-600 dark:text-amber-400" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Ontology-Driven Causal Reasoning
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            AI reasoning grounded in oilfield domain knowledge
          </p>
        </div>
      </div>

      {/* Causal Chain Visualization */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/10 dark:to-orange-900/10 rounded-lg p-6 mb-4">
        <div className="flex items-center justify-center space-x-4">
          <div className="flex-1 text-center">
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-sm border border-amber-200 dark:border-amber-700">
              <p className="text-xs font-semibold text-amber-600 dark:text-amber-400 mb-1">OBSERVATION</p>
              <p className="text-sm font-medium text-slate-900 dark:text-white">
                Production Anomaly
              </p>
            </div>
          </div>

          <ArrowRight className="w-6 h-6 text-amber-500 flex-shrink-0" />

          <div className="flex-1 text-center">
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-sm border border-amber-200 dark:border-amber-700">
              <p className="text-xs font-semibold text-amber-600 dark:text-amber-400 mb-1">CAUSE</p>
              <p className="text-sm font-medium text-slate-900 dark:text-white">
                Equipment Fault
              </p>
            </div>
          </div>

          <ArrowRight className="w-6 h-6 text-amber-500 flex-shrink-0" />

          <div className="flex-1 text-center">
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-sm border border-amber-200 dark:border-amber-700">
              <p className="text-xs font-semibold text-amber-600 dark:text-amber-400 mb-1">EFFECT</p>
              <p className="text-sm font-medium text-slate-900 dark:text-white">
                Production Drop
              </p>
            </div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-amber-700 dark:text-amber-400 font-mono bg-amber-100 dark:bg-amber-900/40 inline-block px-3 py-1 rounded">
            Ontology Rule: {ruleId} - {ruleName}
          </p>
        </div>
      </div>

      {/* Explanation */}
      <div className="space-y-4">
        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-2 flex items-center">
            <span className="mr-2">💡</span>
            Causal Explanation
          </h3>
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
            {ontologyStep.causal_explanation}
          </p>
        </div>

        {ontologyStep.domain_knowledge && (
          <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-2 flex items-center">
              <BookOpen className="w-4 h-4 mr-2" />
              Domain Knowledge
            </h3>
            <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed italic">
              {ontologyStep.domain_knowledge}
            </p>
          </div>
        )}

        {/* Confidence Meter */}
        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">
              Reasoning Confidence
            </h3>
            <span className="text-lg font-bold text-amber-600 dark:text-amber-400">
              {(confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-amber-500 to-orange-500 h-3 rounded-full transition-all duration-500"
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">
            Based on formal ontology rules and domain expertise
          </p>
        </div>
      </div>

      {/* Info Box */}
      <div className="mt-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
        <p className="text-xs text-blue-800 dark:text-blue-300">
          <strong>What is Ontology-Driven Reasoning?</strong> The system uses a formal knowledge model
          of oilfield operations to understand causal relationships between events. This goes beyond
          simple pattern matching to provide explanations grounded in domain expertise.
        </p>
      </div>
    </div>
  );
}

