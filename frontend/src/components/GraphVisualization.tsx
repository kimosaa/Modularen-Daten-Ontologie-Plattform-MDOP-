/**
 * Graph Visualization Component
 * D3.js-based interactive graph viewer
 */
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { GraphData, GraphNode, GraphEdge } from '@types/ontology';

interface GraphVisualizationProps {
  data: GraphData;
  width?: number;
  height?: number;
  onNodeClick?: (node: GraphNode) => void;
  onEdgeClick?: (edge: GraphEdge) => void;
}

export const GraphVisualization: React.FC<GraphVisualizationProps> = ({
  data,
  width = 1200,
  height = 800,
  onNodeClick,
  onEdgeClick,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    if (!svgRef.current || !data.nodes.length) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current);

    // Add zoom behavior
    const g = svg.append('g');
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });
    svg.call(zoom as any);

    // Create force simulation
    const simulation = d3.forceSimulation<GraphNode>(data.nodes)
      .force('link', d3.forceLink<GraphNode, GraphEdge>(data.edges)
        .id((d) => d.id)
        .distance(150))
      .force('charge', d3.forceManyBody().strength(-500))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(60));

    // Create links
    const link = g.append('g')
      .selectAll('line')
      .data(data.edges)
      .join('line')
      .attr('class', 'link')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        event.stopPropagation();
        onEdgeClick?.(d);
      });

    // Create link labels
    const linkLabels = g.append('g')
      .selectAll('text')
      .data(data.edges)
      .join('text')
      .attr('class', 'link-label')
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', '#666')
      .text((d) => d.label || d.type);

    // Create nodes
    const node = g.append('g')
      .selectAll('g')
      .data(data.nodes)
      .join('g')
      .attr('class', 'node')
      .style('cursor', 'pointer')
      .call(d3.drag<SVGGElement, GraphNode>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended) as any);

    // Node circles
    node.append('circle')
      .attr('r', 30)
      .attr('fill', (d) => {
        const colors: Record<string, string> = {
          Person: '#3B82F6',
          Company: '#10B981',
          Location: '#F59E0B',
          default: '#6B7280'
        };
        return colors[d.type] || colors.default;
      })
      .attr('stroke', (d) => selectedNode === d.id ? '#EF4444' : '#fff')
      .attr('stroke-width', (d) => selectedNode === d.id ? 3 : 1.5)
      .on('click', (event, d) => {
        event.stopPropagation();
        setSelectedNode(d.id);
        onNodeClick?.(d);
      });

    // Node labels
    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '12px')
      .attr('font-weight', 'bold')
      .attr('fill', '#fff')
      .attr('pointer-events', 'none')
      .text((d) => d.label.substring(0, 10));

    // Node type badges
    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '2.5em')
      .attr('font-size', '9px')
      .attr('fill', '#333')
      .attr('background', '#fff')
      .text((d) => d.type);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      linkLabels
        .attr('x', (d: any) => (d.source.x + d.target.x) / 2)
        .attr('y', (d: any) => (d.source.y + d.target.y) / 2);

      node.attr('transform', (d) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event: any, d: GraphNode) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.x = event.x;
      d.y = event.y;
    }

    function dragged(event: any, d: GraphNode) {
      d.x = event.x;
      d.y = event.y;
    }

    function dragended(event: any, d: GraphNode) {
      if (!event.active) simulation.alphaTarget(0);
    }

    return () => {
      simulation.stop();
    };
  }, [data, width, height, selectedNode, onNodeClick, onEdgeClick]);

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      style={{ border: '1px solid #e5e7eb', borderRadius: '8px', background: '#f9fafb' }}
    />
  );
};
