import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Zap, Lock, FileText, Database, AlertCircle, CheckCircle } from 'lucide-react';

export default function EnterpriseRAGUI() {
  const [currentUser, setCurrentUser] = useState('doctor_ramesh');
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [step, setStep] = useState(0);

  const users = {
    doctor_ramesh: { name: 'Dr. Ramesh', role: 'doctor', department: 'Medical', avatar: '👨‍⚕️' },
    hr_priya: { name: 'Priya Sharma', role: 'hr', department: 'HR', avatar: '👩‍💼' },
    admin_root: { name: 'Root Admin', role: 'admin', department: 'IT', avatar: '🔐' },
    engineer_john: { name: 'John Dev', role: 'engineer', department: 'Engineering', avatar: '👨‍💻' },
    intern_jane: { name: 'Jane Intern', role: 'intern', department: 'Operations', avatar: '👨‍🎓' },
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStep(0);

    // Simulate query processing with steps
    const steps = [
      'Authenticating user...',
      'Processing query...',
      'Searching documents...',
      'Checking permissions...',
      'Validating answer...',
    ];

    for (let i = 0; i < steps.length; i++) {
      setStep(i);
      await new Promise((r) => setTimeout(r, 600));
    }

    // Mock result
    const mockResult = {
      answer:
        'John के lab report में Hemoglobin की value 14.2 g/dL है और WBC की value 7000 है। Status normal है।',
      confidence: 0.637,
      sources: ['PDF_001', 'CSV_001', 'SQL_001'],
      timestamp: new Date().toISOString(),
      accessible: 3,
      denied: 2,
      total: 5,
    };

    setResults(mockResult);
    setIsLoading(false);
  };

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5 },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-cyan-400" />
            <div>
              <h1 className="text-2xl font-bold text-white">Enterprise RAG</h1>
              <p className="text-xs text-slate-400">Intelligence Platform</p>
            </div>
          </motion.div>

          {/* User Profile */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4 bg-slate-700/50 px-4 py-2 rounded-lg border border-slate-600"
          >
            <span className="text-2xl">{users[currentUser].avatar}</span>
            <div>
              <p className="text-white font-semibold text-sm">{users[currentUser].name}</p>
              <p className="text-cyan-400 text-xs">{users[currentUser].role.toUpperCase()}</p>
            </div>
          </motion.div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <motion.div {...fadeInUp} className="mb-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-3">Intelligent Enterprise Data Retrieval</h2>
          <p className="text-lg text-slate-300">
            Search across PDFs, Databases, JSONs & SQL with role-based security in seconds
          </p>
          <p className="text-cyan-400 mt-3 font-medium">
            🚀 Smart Enterprise RAG: Secure Retrieval That Never Hallucinates
          </p>
        </motion.div>

        {/* Stats Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12 p-6 bg-cyan-500/10 border border-cyan-400 rounded-lg">
          <div className="text-center">
            <h3 className="text-3xl font-bold text-cyan-400">100%</h3>
            <p className="text-slate-300 text-sm mt-2">Factual Answers</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-bold text-cyan-400">4+</h3>
            <p className="text-slate-300 text-sm mt-2">Data Sources</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-bold text-cyan-400">5+</h3>
            <p className="text-slate-300 text-sm mt-2">User Roles</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-bold text-cyan-400">⚡</h3>
            <p className="text-slate-300 text-sm mt-2">Enterprise-Grade</p>
          </div>
        </motion.div>

        {/* Use Cases Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Use Cases</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: '🏥', title: 'Healthcare', desc: 'Patient records & lab reports with confidentiality control' },
              { icon: '👥', title: 'HR & Employee Mgmt', desc: 'Employee data access with privacy compliance' },
              { icon: '📊', title: 'Finance & Compliance', desc: 'Financial data with role-based restrictions' },
              { icon: '⚙️', title: 'Engineering Teams', desc: 'Documentation, logs, configurations securely' },
            ].map((useCase, i) => (
              <motion.div
                key={i}
                whileHover={{ y: -5 }}
                className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 hover:border-cyan-400 transition"
              >
                <p className="text-3xl mb-2">{useCase.icon}</p>
                <p className="text-white font-semibold text-sm mb-1">{useCase.title}</p>
                <p className="text-slate-400 text-xs leading-relaxed">{useCase.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">How It Works</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { num: '1', title: 'Authenticate', desc: 'User & role verification' },
              { num: '2', title: 'Process', desc: 'Intent extraction' },
              { num: '3', title: 'Search', desc: 'Multi-source retrieval' },
              { num: '4', title: 'Filter', desc: 'RBAC enforcement' },
              { num: '5', title: 'Validate', desc: 'Grounding check' },
              { num: '6', title: 'Generate', desc: 'LLM answer' },
            ].map((step, i) => (
              <motion.div
                key={i}
                whileHover={{ scale: 1.05 }}
                className="bg-slate-700/30 border border-slate-600 rounded-lg p-3 text-center hover:border-cyan-400 transition"
              >
                <div className="w-8 h-8 bg-cyan-500 text-slate-900 rounded-full flex items-center justify-center font-bold mx-auto mb-2">
                  {step.num}
                </div>
                <p className="text-white font-semibold text-xs mb-1">{step.title}</p>
                <p className="text-slate-400 text-xs">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          {/* Sidebar Stats */}
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="lg:col-span-1">
            <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-6 space-y-6">
              <div>
                <h3 className="text-slate-300 font-semibold text-sm mb-4">📊 Data Sources</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">📄 PDFs</span>
                    <span className="text-cyan-400 font-semibold">3</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">📊 CSVs</span>
                    <span className="text-cyan-400 font-semibold">3</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">📋 JSONs</span>
                    <span className="text-cyan-400 font-semibold">3</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">🗄️ SQLs</span>
                    <span className="text-cyan-400 font-semibold">2</span>
                  </div>
                </div>
              </div>

              <div className="border-t border-slate-600 pt-4">
                <h3 className="text-slate-300 font-semibold text-sm mb-3">🎭 Switch User</h3>
                <select
                  value={currentUser}
                  onChange={(e) => setCurrentUser(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-cyan-400"
                >
                  {Object.entries(users).map(([id, user]) => (
                    <option key={id} value={id}>
                      {user.avatar} {user.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="border-t border-slate-600 pt-4">
                <h3 className="text-slate-300 font-semibold text-sm mb-3">🔐 Your Access</h3>
                <div className="space-y-2 text-xs">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-400" />
                    <span className="text-slate-300">Patient Records</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-red-400" />
                    <span className="text-slate-400">Financial Data</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Main Content */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="lg:col-span-3">
            {/* Query Section */}
            <div className="bg-gradient-to-br from-slate-700/30 to-slate-800/30 border border-slate-600 rounded-xl p-8 mb-8">
              <form onSubmit={handleQuery} className="space-y-4">
                <div>
                  <label className="block text-sm text-slate-400 mb-2">What would you like to know?</label>
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask me anything about your data..."
                    className="w-full bg-slate-800 border-2 border-slate-600 rounded-lg px-6 py-4 text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:border-2 transition-colors"
                  />
                </div>

                {/* Quick suggestions */}
                <div className="flex flex-wrap gap-2">
                  {currentUser === 'doctor_ramesh' && (
                    <button
                      type="button"
                      onClick={() => setQuery("John ke lab report mein kya likha hai?")}
                      className="px-3 py-1 text-xs bg-slate-700 hover:bg-slate-600 text-cyan-400 rounded transition"
                    >
                      Patient Report
                    </button>
                  )}
                  {currentUser === 'admin_root' && (
                    <button
                      type="button"
                      onClick={() => setQuery("Compliance status kya hai?")}
                      className="px-3 py-1 text-xs bg-slate-700 hover:bg-slate-600 text-cyan-400 rounded transition"
                    >
                      Compliance Check
                    </button>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isLoading || !query}
                  className="w-full bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }}>
                        🔍
                      </motion.div>
                      Searching...
                    </>
                  ) : (
                    <>🔍 Search</>
                  )}
                </button>
              </form>

              {/* Status Indicators */}
              {isLoading && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-6 space-y-2">
                  {['Authenticating...', 'Processing...', 'Retrieving...', 'Validating...', 'Complete...'].map(
                    (text, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: i <= step ? 1 : 0.3, x: 0 }}
                        className={`text-sm ${i <= step ? 'text-cyan-400' : 'text-slate-500'}`}
                      >
                        {i <= step ? '✓' : '○'} {text}
                      </motion.div>
                    )
                  )}
                </motion.div>
              )}
            </div>

            {/* Results Section */}
            {results && !isLoading && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                {/* Answer Card */}
                <div className="bg-slate-700/30 border border-slate-600 rounded-xl p-8">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-white font-semibold">💬 Answer</h3>
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        results.confidence > 0.85
                          ? 'bg-green-500/20 text-green-400'
                          : results.confidence > 0.7
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : 'bg-orange-500/20 text-orange-400'
                      }`}
                    >
                      {(results.confidence * 100).toFixed(1)}% Confidence
                    </motion.div>
                  </div>
                  <p className="text-slate-200 leading-relaxed text-lg">{results.answer}</p>
                  <p className="text-slate-500 text-xs mt-4">{new Date(results.timestamp).toLocaleString()}</p>
                </div>

                {/* Sources */}
                <div>
                  <h3 className="text-white font-semibold mb-4">📎 Information Retrieved From</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {results.sources.map((source, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="bg-slate-700/30 border border-slate-600 rounded-lg p-4"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl">📄</span>
                          <span className="text-white font-semibold text-sm">{source}</span>
                        </div>
                        <div className="flex justify-between text-xs text-slate-400">
                          <span>Relevance: 85%</span>
                          <span className="text-cyan-400">Accessible ✓</span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Audit Log */}
                <details className="bg-slate-700/30 border border-slate-600 rounded-lg p-4">
                  <summary className="cursor-pointer text-white font-semibold flex items-center gap-2">
                    🔐 Security Audit Log
                  </summary>
                  <div className="mt-4 text-sm text-slate-300 space-y-2">
                    <div className="flex justify-between">
                      <span>User:</span>
                      <span className="text-cyan-400">{currentUser}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Documents Retrieved:</span>
                      <span className="text-cyan-400">{results.total}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Accessible:</span>
                      <span className="text-green-400">✓ {results.accessible}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Denied:</span>
                      <span className="text-red-400">✗ {results.denied}</span>
                    </div>
                  </div>
                </details>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Security Highlights */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { icon: '🔐', title: 'Role-Based Access', desc: 'Users only see authorized data' },
            { icon: '🛡️', title: 'Hallucination Prevention', desc: '100% factual answers' },
            { icon: '📝', title: 'Audit Trails', desc: 'Complete compliance logging' },
            { icon: '⚡', title: 'Multi-Source', desc: 'PDFs, DBs, JSONs & SQL' },
          ].map((feature, i) => (
            <motion.div
              key={i}
              whileHover={{ y: -5 }}
              className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 text-center hover:border-cyan-400 transition"
            >
              <p className="text-3xl mb-2">{feature.icon}</p>
              <p className="text-white font-semibold text-sm mb-1">{feature.title}</p>
              <p className="text-slate-400 text-xs">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Footer */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="mt-12 text-center border-t border-slate-700 pt-8">
          <div className="flex justify-center gap-4 mb-4 flex-wrap">
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300 text-sm">📌 GitHub Repository</a>
            <span className="text-slate-600">•</span>
            <a href="#" className="text-cyan-400 hover:text-cyan-300 text-sm">📚 Documentation</a>
            <span className="text-slate-600">•</span>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300 text-sm">🔗 LinkedIn</a>
            <span className="text-slate-600">•</span>
            <a href="#" className="text-cyan-400 hover:text-cyan-300 text-sm">📧 Contact</a>
          </div>
          <p className="text-slate-400 text-sm">
            🚀 Enterprise RAG Intelligence Platform • Powered by Groq AI • Production-Ready
          </p>
          <p className="text-slate-500 text-xs mt-2">Built with Python, Flask, LLMs & Modern Web Technologies</p>
        </motion.div>
      </div>
    </div>
  );
}
