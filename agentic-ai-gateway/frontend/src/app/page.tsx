'use client';

import ThreeScene from '@/components/ThreeScene';
import ServiceCards from '@/components/ServiceCards';

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* Three.js Background */}
      <ThreeScene />
      
      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="p-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
            Agentic AI Gateway
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Enterprise-grade AI platform for tier-1 financial institutions
          </p>
          <div className="mt-6 flex justify-center gap-4">
            <a 
              href="/docs" 
              className="px-6 py-3 bg-white/10 backdrop-blur-lg rounded-full border border-white/20 hover:bg-white/20 transition-all"
            >
              Documentation
            </a>
            <a 
              href="/docs" 
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full hover:from-blue-600 hover:to-purple-600 transition-all"
            >
              Get Started
            </a>
          </div>
        </header>

        {/* Services Grid */}
        <section>
          <h2 className="text-3xl font-bold text-white text-center mb-8">
            AI Services
          </h2>
          <ServiceCards />
        </section>

        {/* Footer */}
        <footer className="p-8 text-center text-gray-400 border-t border-white/10 mt-12">
          <p>Built for enterprise • Python 3.12+ • FastAPI • Next.js • Three.js</p>
          <p className="mt-2 text-sm">© 2024 Agentic AI Gateway. All rights reserved.</p>
        </footer>
      </div>
    </main>
  );
}
