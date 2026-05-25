import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import { Activity, Shield, TrendingUp, AlertCircle, Users, Code, DollarSign, Search, Menu, Bell, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:8000/api/v1/company/nexus-ai/health');
        setData(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch intelligence report. Ensure backend is running.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatHealthData = (score) => {
    if (!score) return [];
    return [
      { subject: 'Strategic Coherence', A: score.strategic_coherence.score * 100 },
      { subject: 'Org Vitality', A: score.org_vitality.score * 100 },
      { subject: 'Tech Foundation', A: score.tech_foundation.score * 100 },
      { subject: 'Financial Resilience', A: score.financial_resilience.score * 100 },
      { subject: 'Talent Dynamics', A: score.talent_dynamics.score * 100 },
      { subject: 'Competitive Position', A: score.competitive_position.score * 100 },
      { subject: 'Dependency Robustness', A: score.dependency_robustness.score * 100 },
    ];
  };

  const formatTrajectoryData = (dist) => {
    if (!dist) return [];
    return [
      { name: 'Growth', prob: dist.growth_prob * 100 },
      { name: 'Stable', prob: dist.stable_prob * 100 },
      { name: 'Pivot', prob: dist.pivot_prob * 100 },
      { name: 'Decline', prob: dist.decline_prob * 100 },
      { name: 'Collapse', prob: dist.collapse_prob * 100 },
    ];
  };

  if (loading) {
    return (
      <div className="main-content" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', flexDirection: 'column', gap: '20px' }}>
        <Loader2 className="animate-spin" size={48} color="var(--accent-primary)" />
        <p style={{ color: 'var(--text-muted)' }}>Synchronsizing multi-agent swarm signals...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="main-content" style={{ padding: '40px' }}>
        <div className="glass card" style={{ borderColor: 'var(--danger)', padding: '40px', textAlign: 'center' }}>
          <AlertCircle size={48} color="var(--danger)" style={{ margin: '0 auto 20px' }} />
          <h3>Connection Failed</h3>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="glass" style={{ marginTop: '20px', padding: '8px 20px', color: 'var(--accent-primary)' }}>Retry Connection</button>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
        <div>
          <h1 className="gradient-text" style={{ fontSize: '2.5rem', margin: 0 }}>{data.company_id.toUpperCase()} Intelligence</h1>
          <p style={{ color: 'var(--text-muted)' }}>Synthesis generated at {new Date(data.timestamp).toLocaleString()}</p>
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
            <span className="badge badge-success">Confidence: {(data.confidence * 100).toFixed(0)}%</span>
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={formatHealthData(data)}>
                <PolarGrid stroke="var(--border-color)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
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
            <span className="badge badge-warning">Shelf Life: {data.shelf_life_days} Days</span>
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={formatTrajectoryData(data.trajectory_1yr)} layout="vertical">
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={80} tick={{ fill: 'var(--text-muted)' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--panel-bg)', borderColor: 'var(--border-color)', borderRadius: '8px', color: 'white' }}
                />
                <Bar dataKey="prob" radius={[0, 4, 4, 0]}>
                  {formatTrajectoryData(data.trajectory_1yr).map((entry, index) => (
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
          <h3>Synthesis Evidence</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '20px' }}>
            {data.evidence_summary.map((ev, i) => (
              <div key={i} className="glass" style={{ padding: '16px', display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                <AlertCircle color="var(--warning)" size={24} />
                <div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600 }}>Signal {i+1}</span>
                    <span className="badge badge-warning" style={{ fontSize: '0.6rem' }}>CONFIRMED</span>
                  </div>
                  <p style={{ margin: '4px 0', color: 'var(--text-muted)', fontSize: '0.9rem' }}>{ev}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass card">
          <h3>Core Composite</h3>
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', fontWeight: 700, color: data.composite_score > 0.7 ? 'var(--success)' : 'var(--warning)' }}>{(data.composite_score * 10).toFixed(1)}</div>
            <p style={{ color: 'var(--text-muted)' }}>Composite Health Index</p>
            <div className={`badge ${data.composite_score > 0.7 ? 'badge-success' : 'badge-warning'}`}>
              {data.composite_score > 0.7 ? 'Robust' : 'Under Review'}
            </div>
            <p style={{ fontSize: '0.8rem', marginTop: '16px', textAlign: 'left' }}>
              Base assumption: {data.assumptions[0]}
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

