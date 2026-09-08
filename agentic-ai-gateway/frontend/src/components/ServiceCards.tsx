'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { services } from '@/lib/api';
import { 
  Shield, 
  FileCode, 
  Database, 
  Server, 
  TrendingUp, 
  Code2, 
  Lock, 
  Bug, 
  TestTube2 
} from 'lucide-react';

const aiServices = [
  {
    id: 'compliance',
    name: 'AutoCompliance Inspector',
    description: 'Automated regulatory compliance checking (SOX, PCI-DSS)',
    icon: Shield,
    color: 'from-blue-500 to-cyan-500',
    endpoint: '/compliance/scan'
  },
  {
    id: 'contract',
    name: 'Smart Contract Analyzer',
    description: 'Blockchain contract security auditing',
    icon: FileCode,
    color: 'from-purple-500 to-pink-500',
    endpoint: '/contract/analyze'
  },
  {
    id: 'governance',
    name: 'Data Governance Orchestrator',
    description: 'GDPR/CCPA compliant data management',
    icon: Database,
    color: 'from-green-500 to-emerald-500',
    endpoint: '/governance/classify'
  },
  {
    id: 'infrastructure',
    name: 'Predictive Infrastructure Monitor',
    description: 'Cloud infrastructure failure prediction',
    icon: Server,
    color: 'from-orange-500 to-red-500',
    endpoint: '/infrastructure/monitor'
  },
  {
    id: 'risk',
    name: 'Financial Risk Assessment',
    description: 'Real-time risk evaluation and scoring',
    icon: TrendingUp,
    color: 'from-yellow-500 to-orange-500',
    endpoint: '/risk/evaluate'
  },
  {
    id: 'review',
    name: 'Code Review Companion',
    description: 'Intelligent PR reviewer',
    icon: Code2,
    color: 'from-indigo-500 to-purple-500',
    endpoint: '/review/pr'
  },
  {
    id: 'security',
    name: 'API Security Sentinel',
    description: 'Automated API vulnerability scanner',
    icon: Lock,
    color: 'from-red-500 to-rose-500',
    endpoint: '/security/scan'
  },
  {
    id: 'debug',
    name: 'Intelligent Debugging Assistant',
    description: 'AI-powered debugging tool',
    icon: Bug,
    color: 'from-teal-500 to-cyan-500',
    endpoint: '/debug/analyze'
  },
  {
    id: 'tests',
    name: 'Test Case Generator',
    description: 'Comprehensive test suite creation',
    icon: TestTube2,
    color: 'from-pink-500 to-rose-500',
    endpoint: '/tests/generate'
  }
];

export default function ServiceCards() {
  const [loading, setLoading] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, any>>({});

  const handleServiceClick = async (serviceId: string) => {
    setLoading(serviceId);
    try {
      // Demo request - in production, send actual data
      const response = await services.getStatus();
      setResults(prev => ({ ...prev, [serviceId]: response.data }));
    } catch (error) {
      console.error(`Error calling ${serviceId}:`, error);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8">
      {aiServices.map((service, index) => (
        <motion.div
          key={service.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.05 }}
          className={`bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 cursor-pointer hover:bg-white/20 transition-all`}
          onClick={() => handleServiceClick(service.id)}
        >
          <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${service.color} flex items-center justify-center mb-4`}>
            <service.icon className="w-7 h-7 text-white" />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">{service.name}</h3>
          <p className="text-gray-300 text-sm mb-4">{service.description}</p>
          <code className="text-xs text-gray-400 bg-black/30 px-2 py-1 rounded">
            POST {service.endpoint}
          </code>
          {loading === service.id && (
            <div className="mt-4 text-blue-400 text-sm">Processing...</div>
          )}
          {results[service.id] && (
            <div className="mt-4 text-green-400 text-sm">
              ✓ Service available
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
}
