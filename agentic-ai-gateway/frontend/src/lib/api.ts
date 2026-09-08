import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const services = {
  // Get gateway status
  getStatus: () => api.get('/status'),
  
  // Compliance Inspector
  scanCompliance: (data: any) => api.post('/compliance/scan', data),
  
  // Smart Contract Analyzer
  analyzeContract: (data: any) => api.post('/contract/analyze', data),
  
  // Data Governance
  classifyData: (data: any) => api.post('/governance/classify', data),
  
  // Infrastructure Monitor
  monitorInfrastructure: (data: any) => api.get('/infrastructure/monitor', { params: data }),
  
  // Risk Assessment
  evaluateRisk: (data: any) => api.post('/risk/evaluate', data),
  
  // Code Review
  reviewPR: (data: any) => api.post('/review/pr', data),
  
  // API Security
  scanAPISecurity: (data: any) => api.post('/security/scan', data),
  
  // Debugging Assistant
  analyzeDebug: (data: any) => api.post('/debug/analyze', data),
  
  // Test Generation
  generateTests: (data: any) => api.post('/tests/generate', data),
};
