import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../api/axios';
import { Users, GraduationCap, School, ArrowUpRight, Activity, Calendar, Bell, Search } from 'lucide-react';
import AIWidget from '../components/AIWidget';

const AdminDashboard = () => {
  const userName = localStorage.getItem('user_name') || 'Admin';

  const [stats, setStats] = useState({
    total_students: 0,
    total_teachers: 0,
    total_users: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/users/dashboard_stats');
        setStats(response.data);
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    };

    fetchStats();
  }, []);

  const StatCard = ({ title, count, icon: Icon, color, gradient }) => (
    <div className="relative overflow-hidden bg-white/5 backdrop-blur-md border border-white/10 rounded-3xl p-6 transition-all duration-300 hover:-translate-y-1 hover:bg-white/10 group">
      <div className={`absolute -right-6 -top-6 w-32 h-32 rounded-full blur-3xl opacity-20 group-hover:opacity-30 transition-opacity ${gradient}`}></div>

      <div className="relative z-10">
        <div className="flex justify-between items-start mb-4">
          <div className={`p-3 rounded-2xl bg-white/5 border border-white/10 text-white group-hover:scale-110 transition-transform duration-300`}>
            <Icon size={24} className={color} />
          </div>
          <div className="flex items-center gap-1 text-emerald-400 bg-emerald-400/10 border border-emerald-400/20 px-2 py-1 rounded-lg">
            <ArrowUpRight size={12} strokeWidth={3} />
            <span className="text-[10px] font-bold">+12%</span>
          </div>
        </div>

        <h3 className="text-gray-400 font-medium text-xs uppercase tracking-widest mb-1">{title}</h3>
        <span className="text-4xl font-bold text-white tracking-tight">{count}</span>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-dark-900 font-sans text-gray-300 selection:bg-accent-purple selection:text-white">
      <Sidebar />

      <div className="flex-1 p-8 overflow-y-auto w-full relative">
        {/* Background Gradients */}
        <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
          <div className="absolute top-[-10%] left-[20%] w-[500px] h-[500px] bg-accent-purple/20 rounded-full blur-[120px]"></div>
          <div className="absolute bottom-[-10%] right-[10%] w-[400px] h-[400px] bg-accent-blue/10 rounded-full blur-[100px]"></div>
        </div>

        <div className="relative z-10">
          {/* Header */}
          <header className="flex justify-between items-center mb-10 animate-in fade-in slide-in-from-top-4 duration-500">
            <div>
              <h2 className="text-3xl font-bold text-white tracking-tight">Dashboard</h2>
              <p className="text-gray-400 mt-1">Welcome back, <span className="text-white font-semibold">{userName}</span> 👋</p>
            </div>

            <div className="flex items-center gap-4">
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
                <input type="text" placeholder="Search..." className="bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-accent-purple/50 focus:ring-1 focus:ring-accent-purple/50 transition-all w-64" />
              </div>
              <button className="p-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 transition-all relative">
                <Bell size={20} />
                <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-accent-pink rounded-full shadow-[0_0_10px_#ec4899]"></span>
              </button>
              <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-accent-purple to-accent-blue p-[1px] cursor-pointer">
                <img
                  src={`https://ui-avatars.com/api/?name=${userName}&background=000&color=fff`}
                  alt="Profile"
                  className="rounded-[10px] h-full w-full object-cover bg-dark-800"
                />
              </div>
            </div>
          </header>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-100">
            <StatCard
              title="Total Students"
              count={stats.total_students}
              icon={GraduationCap}
              color="text-accent-blue"
              gradient="bg-accent-blue"
            />
            <StatCard
              title="Total Teachers"
              count={stats.total_teachers}
              icon={School}
              color="text-emerald-400"
              gradient="bg-emerald-400"
            />
            <StatCard
              title="System Users"
              count={stats.total_users}
              icon={Users}
              color="text-accent-purple"
              gradient="bg-accent-purple"
            />
          </div>

          {/* Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-8 duration-500 delay-200">

            {/* Recent Activity */}
            <div className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Activity className="text-accent-purple" size={20} />
                  Recent Activity
                </h3>
                <button className="text-xs font-bold text-gray-400 hover:text-white hover:bg-white/5 px-3 py-1.5 rounded-lg transition-colors uppercase tracking-wider">View All</button>
              </div>

              <div className="space-y-2">
                {[1, 2, 3, 4].map((_, i) => (
                  <div key={i} className="flex items-center justify-between p-4 hover:bg-white/5 rounded-2xl transition-all cursor-pointer group border border-transparent hover:border-white/5">
                    <div className="flex items-center gap-4">
                      <div className="h-10 w-10 bg-white/5 rounded-xl flex items-center justify-center text-gray-400 group-hover:bg-accent-purple/20 group-hover:text-accent-purple transition-all">
                        <Users size={18} />
                      </div>
                      <div>
                        <p className="font-semibold text-gray-200 group-hover:text-white transition-colors text-sm">New User Registered</p>
                        <p className="text-xs text-gray-500 font-medium">System updated with new enrollment</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-[10px] font-bold text-gray-500 mb-1">2 MIN AGO</p>
                      <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Upcoming Events */}
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Calendar className="text-accent-pink" size={20} />
                  Upcoming
                </h3>
              </div>

              <div className="space-y-8">
                <div className="relative pl-6 border-l border-white/10 space-y-8">
                  {[1, 2, 3].map((_, i) => (
                    <div key={i} className="relative group cursor-pointer">
                      <span className="absolute -left-[29px] top-1 h-3 w-3 rounded-full border-2 border-dark-900 bg-gray-600 group-hover:bg-accent-pink group-hover:shadow-[0_0_10px_#ec4899] transition-all"></span>
                      <p className="text-[10px] font-bold text-accent-pink mb-1 uppercase tracking-wider">Tomorrow, 10:00 AM</p>
                      <h4 className="font-bold text-gray-200 group-hover:text-white transition-colors">Faculty Meeting</h4>
                      <p className="text-xs text-gray-500 mt-1">Discussion on new semester curriculum.</p>
                    </div>
                  ))}
                </div>
              </div>
              <button className="w-full mt-8 py-3 rounded-xl border border-white/10 text-gray-400 text-sm font-bold hover:bg-white/5 hover:text-white hover:border-white/20 transition-all">
                View Full Calendar
              </button>
            </div>

          </div>
        </div>
      </div>

      <AIWidget />
    </div>
  );
};

export default AdminDashboard;