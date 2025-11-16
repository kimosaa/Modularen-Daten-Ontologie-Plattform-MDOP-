/**
 * Main Application Component
 */
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import { Toaster } from 'react-hot-toast';
import { GraphExplorer } from '@pages/GraphExplorer';

// Create Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Create MUI Theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#3B82F6',
    },
    secondary: {
      main: '#10B981',
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <Toaster position="top-right" />
          <GraphExplorer />
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
