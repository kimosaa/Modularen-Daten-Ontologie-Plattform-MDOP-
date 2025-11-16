/**
 * Graph Explorer Page
 * Main page for exploring and visualizing the knowledge graph
 */
import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Button } from '@mui/material';
import { GraphVisualization } from '@components/GraphVisualization';
import { ontologyService } from '@services/ontology.service';
import { GraphData, GraphNode } from '@types/ontology';

export const GraphExplorer: React.FC = () => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [loading, setLoading] = useState(false);

  const loadSampleData = async () => {
    setLoading(true);
    try {
      // Load sample graph data
      const sampleData: GraphData = {
        nodes: [
          { id: '1', type: 'Person', label: 'John Doe', properties: { age: 30 } },
          { id: '2', type: 'Company', label: 'Acme Corp', properties: { industry: 'Tech' } },
          { id: '3', type: 'Location', label: 'New York', properties: { country: 'USA' } },
        ],
        edges: [
          { id: 'e1', source: '1', target: '2', type: 'WORKS_AT', label: 'Works At', properties: {} },
          { id: 'e2', source: '2', target: '3', type: 'LOCATED_IN', label: 'Located In', properties: {} },
        ],
      };
      setGraphData(sampleData);
    } catch (error) {
      console.error('Failed to load graph data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSampleData();
  }, []);

  const handleNodeClick = (node: GraphNode) => {
    setSelectedNode(node);
  };

  return (
    <Box sx={{ p: 3, height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" gutterBottom>
        MDOP - Graph Explorer
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, flex: 1 }}>
        {/* Graph Visualization */}
        <Paper sx={{ flex: 1, p: 2 }}>
          <GraphVisualization
            data={graphData}
            width={1000}
            height={700}
            onNodeClick={handleNodeClick}
          />
        </Paper>

        {/* Node Details Panel */}
        <Paper sx={{ width: 300, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Node Details
          </Typography>
          {selectedNode ? (
            <Box>
              <Typography><strong>ID:</strong> {selectedNode.id}</Typography>
              <Typography><strong>Type:</strong> {selectedNode.type}</Typography>
              <Typography><strong>Label:</strong> {selectedNode.label}</Typography>
              <Typography><strong>Properties:</strong></Typography>
              <pre style={{ fontSize: '12px' }}>
                {JSON.stringify(selectedNode.properties, null, 2)}
              </pre>
            </Box>
          ) : (
            <Typography color="text.secondary">
              Click on a node to view details
            </Typography>
          )}
        </Paper>
      </Box>
    </Box>
  );
};
