import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Tabs } from '../components/Tabs';
import CareerPathVisualization from './CareerPathVisualization';
import SkillGapAnalyzer from './SkillGapAnalyzer';
import JobMarketAlignment from './JobMarketAlignment';
import { Award, BookOpen, Briefcase, ChevronRight, ExternalLink, Mail, Phone, AlertCircle, Loader } from 'lucide-react';

export default function AIInsightsDashboard({ aiInsights }) {
  const [selectedCourseIdx, setSelectedCourseIdx] = useState(0);
  const [activeTab, setActiveTab] = useState('career');
  const [showApplicationModal, setShowApplicationModal] = useState(false);
  const [isLoading, setIsLoading] = useState(!aiInsights);

  // Ensure we have valid data
  useEffect(() => {
    if (aiInsights && aiInsights.analysis && aiInsights.analysis.length > 0) {
      setIsLoading(false);
    }
  }, [aiInsights]);

  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center py-20"
      >
        <div className="flex flex-col items-center space-y-4">
          <Loader className="w-12 h-12 text-blue-600 animate-spin" />
          <p className="text-lg text-gray-600">Generating AI insights...</p>
        </div>
      </motion.div>
    );
  }

  if (!aiInsights || !aiInsights.analysis || aiInsights.analysis.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center py-20 bg-amber-50 rounded-xl border-2 border-amber-200"
      >
        <div className="flex flex-col items-center space-y-3">
          <AlertCircle className="w-12 h-12 text-amber-600" />
          <p className="text-lg font-semibold text-amber-900">Unable to generate insights</p>
          <p className="text-sm text-amber-700">Please try again with valid course recommendations</p>
        </div>
      </motion.div>
    );
  }

  const currentAnalysis = aiInsights.analysis[selectedCourseIdx];
  const allCourses = aiInsights.analysis;

  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5 }
  };

  const tabs = [
    {
      id: 'career',
      label: '🚀 Career Path',
      icon: Award
    },
    {
      id: 'skills',
      label: '🎓 Skill Gaps',
      icon: BookOpen
    },
    {
      id: 'market',
      label: '📊 Job Market',
      icon: Briefcase
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="w-full"
    >
      {/* Header */}
      <motion.div variants={fadeIn} className="mb-8">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text mb-2">
          🤖 AI-Powered Insights
        </h2>
        <p className="text-gray-600 text-lg">
          Comprehensive analysis of your top course recommendations
        </p>
      </motion.div>

      {/* Course Selection Tabs */}
      <motion.div variants={fadeIn} className="mb-8">
        <p className="text-sm font-bold text-gray-600 mb-4 uppercase">Select a Course to Analyze</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {allCourses.map((analysis, idx) => (
            <motion.button
              key={idx}
              onClick={() => setSelectedCourseIdx(idx)}
              className={`p-4 rounded-xl border-2 transition-all text-left group ${
                selectedCourseIdx === idx
                  ? 'bg-gradient-to-br from-blue-500 to-purple-500 border-blue-600 shadow-lg'
                  : 'bg-white border-gray-200 hover:border-blue-300'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className={`text-sm font-bold mb-1 ${selectedCourseIdx === idx ? 'text-white' : 'text-gray-600'}`}>
                    #{analysis.rank}
                  </p>
                  <h4 className={`font-bold mb-2 line-clamp-2 ${selectedCourseIdx === idx ? 'text-white' : 'text-gray-900'}`}>
                    {analysis.course}
                  </h4>
                  <p className={`text-sm ${selectedCourseIdx === idx ? 'text-blue-100' : 'text-gray-600'}`}>
                    Match: <span className="font-bold">{Math.round(analysis.match_score * 100)}%</span>
                  </p>
                </div>
                <div className={`text-2xl transition-transform group-hover:translate-x-1 ${selectedCourseIdx === idx ? 'opacity-100' : 'opacity-0'}`}>
                  <ChevronRight className="w-6 h-6 text-white" />
                </div>
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Analysis Tabs */}
      <motion.div variants={fadeIn} className="mb-8">
        <div className="flex space-x-2 mb-8 border-b border-gray-200">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-4 font-bold text-lg transition-all relative ${
                  isActive
                    ? 'text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
                whileTap={{ scale: 0.95 }}
              >
                {tab.label}
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-purple-600"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
              </motion.button>
            );
          })}
        </div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'career' && (
            <CareerPathVisualization careerPath={currentAnalysis.career_path} />
          )}

          {activeTab === 'skills' && (
            <SkillGapAnalyzer skillAnalysis={currentAnalysis.skill_gaps} />
          )}

          {activeTab === 'market' && (
            <JobMarketAlignment marketData={currentAnalysis.job_market} />
          )}
        </motion.div>
      </motion.div>

      {/* Summary Card */}
      <motion.div
        variants={fadeIn}
        className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 border-2 border-blue-200"
      >
        <h3 className="text-2xl font-bold text-gray-900 mb-6">📋 Quick Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Career Readiness */}
          <div className="bg-white rounded-lg p-6 border border-blue-100">
            <h4 className="text-lg font-bold text-gray-900 mb-3">Career Readiness</h4>
            <p className="text-sm text-gray-600 mb-4">
              {currentAnalysis.skill_gaps.readiness_level}
            </p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                style={{ width: `${currentAnalysis.skill_gaps.readiness_score}%` }}
              ></div>
            </div>
            <p className="text-sm font-bold text-gray-700 mt-2">
              {Math.round(currentAnalysis.skill_gaps.readiness_score)}% Ready
            </p>
          </div>

          {/* Market Opportunity */}
          <div className="bg-white rounded-lg p-6 border border-green-100">
            <h4 className="text-lg font-bold text-gray-900 mb-3">Market Opportunity</h4>
            <p className="text-4xl font-bold text-green-600 mb-2">
              {currentAnalysis.job_market.alignment_score}%
            </p>
            <p className="text-sm text-gray-600">
              {currentAnalysis.job_market.recommendation}
            </p>
          </div>

          {/* Growth Potential */}
          <div className="bg-white rounded-lg p-6 border border-purple-100">
            <h4 className="text-lg font-bold text-gray-900 mb-3">Growth Potential</h4>
            <p className="text-4xl font-bold text-purple-600 mb-2">
              +{currentAnalysis.job_market.growth_rate}%
            </p>
            <p className="text-sm text-gray-600">
              Annual growth in field
            </p>
          </div>
        </div>
      </motion.div>

      {/* Final Recommendation */}
      <motion.div
        variants={fadeIn}
        className="mt-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl p-8 text-white"
      >
        <h3 className="text-2xl font-bold mb-4">✨ Final Recommendation</h3>
        <p className="text-lg text-blue-50 leading-relaxed mb-6">
          Based on comprehensive AI analysis of career paths, skill requirements, and market trends,
          <span className="font-bold text-white block mt-2">
            "{currentAnalysis.course}"
          </span>
          is an excellent choice for your qualifications and career aspirations. With strong job market demand,
          clear career progression, and opportunities to develop essential skills, this course positions you
          well for a successful and rewarding career.
        </p>
        <button 
          onClick={() => setShowApplicationModal(true)}
          className="bg-white text-purple-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition-all transform hover:scale-105"
        >
          Start Your Application →
        </button>
      </motion.div>

      {/* Application Modal */}
      {showApplicationModal && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => setShowApplicationModal(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-2xl p-8 max-w-2xl w-full shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold text-gray-900">
                🎓 Start Your Application
              </h2>
              <button
                onClick={() => setShowApplicationModal(false)}
                className="text-gray-400 hover:text-gray-600 transition"
              >
                ✕
              </button>
            </div>

            <div className="mb-8 p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border-2 border-blue-200">
              <p className="text-lg font-bold text-gray-900 mb-2">Selected Course:</p>
              <p className="text-xl text-blue-600">{currentAnalysis.course}</p>
            </div>

            <div className="space-y-4 mb-8">
              <p className="text-gray-700 font-semibold">Choose how you'd like to proceed:</p>
              
              {/* Online Application */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg font-bold hover:shadow-lg transition-all flex items-center justify-between"
                onClick={() => window.open('https://www.unidirectory.lk/', '_blank')}
              >
                <span className="flex items-center space-x-3">
                  <ExternalLink className="w-5 h-5" />
                  <span>Apply Online - University Portal</span>
                </span>
                <span>→</span>
              </motion.button>

              {/* Email Contact */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full p-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg font-bold hover:shadow-lg transition-all flex items-center justify-between"
                onClick={() => window.location.href = 'mailto:admissions@university.lk'}
              >
                <span className="flex items-center space-x-3">
                  <Mail className="w-5 h-5" />
                  <span>Email Admissions</span>
                </span>
                <span>→</span>
              </motion.button>

              {/* Phone Contact */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full p-4 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-bold hover:shadow-lg transition-all flex items-center justify-between"
                onClick={() => window.location.href = 'tel:+94112123456'}
              >
                <span className="flex items-center space-x-3">
                  <Phone className="w-5 h-5" />
                  <span>Call Admissions Office</span>
                </span>
                <span>→</span>
              </motion.button>
            </div>

            <div className="p-4 bg-amber-50 border-2 border-amber-200 rounded-lg mb-6">
              <p className="text-sm text-amber-800">
                💡 <span className="font-bold">Tip:</span> Most universities have online portals where you can apply directly. Contact them if you need help with the application process.
              </p>
            </div>

            <button
              onClick={() => setShowApplicationModal(false)}
              className="w-full py-3 border-2 border-gray-300 rounded-lg font-bold text-gray-700 hover:bg-gray-50 transition"
            >
              Close
            </button>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  );
}
