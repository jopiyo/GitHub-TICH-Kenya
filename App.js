import React, { useState, useEffect } from 'react';
import RiskMap from './components/RiskMap';
import TrendsChart from './components/TrendsChart';
import { AlertTriangle, Thermometer, Droplets } from 'lucide-react';

function App() {
  const [stats, setStats] = useState({ temp: 28, rain: 45, alertLevel: 'Elevated' });

  return (
    <div className="bg-slate-50 min-h-screen p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">ClimateGuard Dashboard</h1>
        <div className="flex gap-4">
          <div className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-blue-500">
            <p className="text-sm text-slate-500">Current Temp</p>
            <p className="text-xl font-bold">{stats.temp}°C</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-red-500">
            <p className="text-sm text-slate-500">Risk Status</p>
            <p className="text-xl font-bold text-red-600">{stats.alertLevel}</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-4">Regional Risk Heatmap</h2>
          <RiskMap geoData={null} riskLevels={{ "Nyando": 0.9 }} />
        </section>
        
        <section className="bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-4">Climate-Health Correlation</h2>
          <TrendsChart data={[]} />
        </section>
      </div>
    </div>
  );
}

export default App;
