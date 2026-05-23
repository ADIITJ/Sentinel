import React, { useState } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import { Activity, Shield, TrendingUp, AlertCircle, Users, Code, DollarSign, Search, Menu, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

const MOCK_HEALTH = [
  { subject: 'Strategic Coherence', A: 80, fullMark: 100 },
  { subject: 'Org Vitality', A: 70, fullMark: 100 },
  { subject: 'Tech Foundation', A: 90, fullMark: 100 },
  { subject: 'Financial Resilience', A: 60, fullMark: 100 },
  { subject: 'Talent Dynamics', A: 75, fullMark: 100 },
  { subject: 'Competitive Position', A: 85, fullMark: 100 },
  { subject: 'Dependency Robustness', A: 50, fullMark: 100 },
];

const MOCK_TRAJECTORY = [
  { name: 'Growth', prob: 60 },
  { name: 'Stable', prob: 30 },
  { name: 'Pivot', prob: 5 },
  { name: 'Decline', prob: 4 },
  { name: 'Collapse', prob: 1 },
];

const Dashboard = () => {
  return (
    <div className="main-content">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
        <div>
          <h1 className="gradient-text" style={{ fontSize: '2.5rem', margin: 0 }}>Company Health Intelligence</h1>
          <p style={{ color: 'var(--text-muted)' }}>Real-time synthesis of digital exhaust and organizational signals.</p>
        </div>
        <div style={{ display: 'flex', gap: '16px' }}>
          <div className="glass" style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Search size={18} color="var(--text-muted)" />
            <input type="text" placeholder="Search companies..." style={{ background: 'none', border: 'none', color: 'white', outline: 'none' }} />
          </div>
          <button className="glass" style={{ padding: '8px', cursor: 'pointer' }}><Bell size={20} /></button>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Health Radar */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass card"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2>7-Dimension Health Score</h2>
            <span className="badge badge-success">Confidence: 82%</span>
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={MOCK_HEALTH}>
                <PolarGrid stroke="var(--border-color)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                <Radar
                  name="Health"
                  dataKey="A"
                  stroke="var(--accent-primary)"
                  fill="var(--accent-primary)"
                  fillOpacity={0.3}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Trajectory Forecast */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass card"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2>1-Year Trajectory Forecast</h2>
            <span className="badge badge-warning">Stale in 4 days</span>
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={MOCK_TRAJECTORY} layout="vertical">
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={80} tick={{ fill: 'var(--text-muted)' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--panel-bg)', borderColor: 'var(--border-color)', borderRadius: '8px' }}
                />
                <Bar dataKey="prob" radius={[0, 4, 4, 0]}>
                  {MOCK_TRAJECTORY.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? 'var(--success)' : index > 2 ? 'var(--danger)' : 'var(--accent-primary)'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Alerts & Signals */}
      <div style={{ marginTop: '24px', display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        <div className="glass card">
          <h3>Recent Stealth Alerts</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '20px' }}>
            {[
              { type: 'Strategic Pivot', company: 'Nexus AI', desc: 'Sudden shift in hiring for "Edge Inference" specialists detected.', confidence: 'High' },
              { type: 'Talent Flight', company: 'Global Cloud', desc: 'Senior engineering attrition increased by 24% in Q2.', confidence: 'Medium' }
            ].map((alert, i) => (
              <div key={i} className="glass" style={{ padding: '16px', display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                <AlertCircle color="var(--warning)" size={24} />
                <div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600 }}>{alert.company}</span>
                    <span className="badge badge-warning" style={{ fontSize: '0.6rem' }}>{alert.type}</span>
                  </div>
                  <p style={{ margin: '4px 0', color: 'var(--text-muted)', fontSize: '0.9rem' }}>{alert.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass card">
          <h3>Narrative vs Reality</h3>
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', fontWeight: 700, color: 'var(--danger)' }}>0.78</div>
            <p style={{ color: 'var(--text-muted)' }}>Divergence Score</p>
            <div className="badge badge-danger">High Deception Risk</div>
            <p style={{ fontSize: '0.8rem', marginTop: '16px', textAlign: 'left' }}>
              Public narrative focuses on "Growth", but internal signals show infrastructure budget cuts and mass ghost job postings.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Sidebar = () => (
  <aside className="sidebar glass">
    <div style={{ marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '12px' }}>
      <Shield size={32} color="var(--accent-primary)" />
      <span style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '1px' }}>SENTINEL</span>
    </div>
    <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {[
        { icon: Activity, label: 'Dashboard', active: true },
        { icon: TrendingUp, label: 'Market Outlook' },
        { icon: Users, label: 'Talent Dynamics' },
        { icon: Code, label: 'Tech Health' },
        { icon: DollarSign, label: 'Financials' },
        { icon: Shield, label: 'Risk Map' }
      ].map((item, i) => (
        <div key={i} className={`glass`} style={{ 
          padding: '12px 16px', 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px', 
          cursor: 'pointer',
          background: item.active ? 'rgba(0, 242, 255, 0.1)' : 'transparent',
          borderColor: item.active ? 'var(--accent-primary)' : 'transparent'
        }}>
          <item.icon size={20} color={item.active ? 'var(--accent-primary)' : 'var(--text-muted)'} />
          <span style={{ color: item.active ? 'white' : 'var(--text-muted)' }}>{item.label}</span>
        </div>
      ))}
    </nav>
  </aside>
);

function App() {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <Dashboard />
    </div>
  );
}

export default App;
