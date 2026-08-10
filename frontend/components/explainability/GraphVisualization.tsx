'use client';

import { useEffect, useRef } from 'react';
import { GraphVisualization as GraphVisualizationType } from '@/lib/api';
import { Network as NetworkIcon } from 'lucide-react';

interface GraphVisualizationProps {
  graphData: GraphVisualizationType;
}

export default function GraphVisualization({ graphData }: GraphVisualizationProps) {
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!canvasRef.current || !graphData) return;

    // Simple force-directed graph layout
    const width = canvasRef.current.clientWidth;
    const height = 400;

    // Create SVG
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', width.toString());
    svg.setAttribute('height', height.toString());
    svg.setAttribute('class', 'w-full h-full');

    // Position nodes in a circle
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    const nodePositions = new Map<string, { x: number; y: number }>();
    graphData.nodes.forEach((node, idx) => {
      const angle = (idx / graphData.nodes.length) * 2 * Math.PI;
      nodePositions.set(node.id, {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      });
    });

    // Draw edges
    graphData.edges.forEach((edge) => {
      const from = nodePositions.get(edge.from);
      const to = nodePositions.get(edge.to);
      
      if (from && to) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', from.x.toString());
        line.setAttribute('y1', from.y.toString());
        line.setAttribute('x2', to.x.toString());
        line.setAttribute('y2', to.y.toString());
        line.setAttribute('stroke', '#94a3b8');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('marker-end', 'url(#arrowhead)');
        svg.appendChild(line);

        // Edge label
        const midX = (from.x + to.x) / 2;
        const midY = (from.y + to.y) / 2;
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', midX.toString());
        text.setAttribute('y', midY.toString());
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('class', 'text-xs fill-slate-600 dark:fill-slate-400');
        text.textContent = edge.label;
        svg.appendChild(text);
      }
    });

    // Define arrowhead marker
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', 'arrowhead');
    marker.setAttribute('markerWidth', '10');
    marker.setAttribute('markerHeight', '10');
    marker.setAttribute('refX', '9');
    marker.setAttribute('refY', '3');
    marker.setAttribute('orient', 'auto');
    const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    polygon.setAttribute('points', '0 0, 10 3, 0 6');
    polygon.setAttribute('fill', '#94a3b8');
    marker.appendChild(polygon);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // Draw nodes
    graphData.nodes.forEach((node) => {
      const pos = nodePositions.get(node.id);
      if (!pos) return;

      // Node circle
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', pos.x.toString());
      circle.setAttribute('cy', pos.y.toString());
      circle.setAttribute('r', '30');
      
      const nodeColor = 
        node.type === 'Rig' ? '#3b82f6' :
        node.type === 'Well' ? '#10b981' :
        node.type === 'Equipment' ? '#f59e0b' :
        node.status === 'faulty' ? '#ef4444' :
        '#6366f1';
      
      circle.setAttribute('fill', nodeColor);
      circle.setAttribute('class', 'cursor-pointer hover:opacity-80 transition-opacity');
      svg.appendChild(circle);

      // Node label
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', pos.x.toString());
      text.setAttribute('y', (pos.y + 50).toString());
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('class', 'text-sm font-semibold fill-slate-900 dark:fill-white');
      text.textContent = node.label;
      svg.appendChild(text);

      // Node type
      const typeText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      typeText.setAttribute('x', pos.x.toString());
      typeText.setAttribute('y', (pos.y + 65).toString());
      typeText.setAttribute('text-anchor', 'middle');
      typeText.setAttribute('class', 'text-xs fill-slate-600 dark:fill-slate-400');
      typeText.textContent = node.type;
      svg.appendChild(typeText);
    });

    // Clear and append
    canvasRef.current.innerHTML = '';
    canvasRef.current.appendChild(svg);
  }, [graphData]);

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center space-x-2 mb-6">
        <NetworkIcon className="w-6 h-6 text-purple-600 dark:text-purple-400" />
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">
          Knowledge Graph Visualization
        </h2>
      </div>

      {/* Graph Canvas */}
      <div 
        ref={canvasRef}
        className="bg-slate-50 dark:bg-slate-900 rounded-lg border-2 border-slate-200 dark:border-slate-700 overflow-hidden"
        style={{ height: '400px' }}
      />

      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
          <span className="text-sm text-slate-600 dark:text-slate-400">Rig</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-500 rounded-full"></div>
          <span className="text-sm text-slate-600 dark:text-slate-400">Well</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-amber-500 rounded-full"></div>
          <span className="text-sm text-slate-600 dark:text-slate-400">Equipment</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-red-500 rounded-full"></div>
          <span className="text-sm text-slate-600 dark:text-slate-400">Faulty</span>
        </div>
      </div>

      {/* Stats */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Nodes</p>
          <p className="text-xl font-bold text-slate-900 dark:text-white">
            {graphData.nodes.length}
          </p>
        </div>
        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-center">
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Relationships</p>
          <p className="text-xl font-bold text-slate-900 dark:text-white">
            {graphData.edges.length}
          </p>
        </div>
      </div>
    </div>
  );
}

