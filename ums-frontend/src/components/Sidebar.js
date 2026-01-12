import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, GraduationCap, LogOut, Settings, Bell, Command } from 'lucide-react';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const NavItem = ({ path, icon: Icon, label }) => {
    const isActive = location.pathname === path;
    return (
      <button
        onClick={() => navigate(path)}
        className={`w-full flex items-center gap-4 px-4 py-3.5 transition-all duration-300 group relative overflow-hidden rounded-xl mx-2 mb-1 w-[calc(100%-16px)]
          ${isActive
            ? "text-white bg-accent-purple/20 border border-accent-purple/20 shadow-[0_0_15px_rgba(139,92,246,0.3)]"
            : "text-gray-400 hover:text-white hover:bg-white/5"
          }`}
      >
        <Icon size={20} strokeWidth={isActive ? 2.5 : 2} className={`transition-transform duration-300 ${isActive ? 'scale-110 text-accent-purple' : 'group-hover:scale-110 group-hover:text-white'}`} />
        <span className="text-sm font-medium tracking-wide">{label}</span>
        {isActive && <div className="absolute inset-y-0 left-0 w-1 bg-accent-purple rounded-r-full shadow-[0_0_10px_#8b5cf6]" />}
      </button>
    );
  };

  return (
    <div className="w-72 bg-dark-900/50 backdrop-blur-xl border-r border-white/5 h-screen flex flex-col sticky top-0 font-sans z-50">
      {/* Logo Area */}
      <div className="p-6 mb-2 flex items-center gap-3">
        <div className="h-10 w-10 bg-gradient-to-br from-accent-purple to-accent-blue rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(139,92,246,0.3)]">
          <Command className="text-white" size={20} />
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">UMS<span className="text-accent-purple">.</span></h1>
      </div>

      <div className="px-6 mb-4">
        <div className="h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 space-y-1">
        <p className="px-6 text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2 mt-2">Main Menu</p>
        <NavItem path="/admin" icon={LayoutDashboard} label="Dashboard" />
        <NavItem path="/admin/students" icon={GraduationCap} label="Students" />
        <NavItem path="/admin/teachers" icon={Users} label="Teachers" />

        <p className="px-6 text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2 mt-4">System</p>
        <NavItem path="/admin/settings" icon={Settings} label="Settings" />
        <NavItem path="/admin/notifications" icon={Bell} label="Notifications" />
      </nav>

      {/* Logout Area */}
      <div className="p-4 mx-2 mb-4">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3.5 text-gray-400 hover:text-white hover:bg-red-500/10 hover:border-red-500/20 border border-transparent rounded-xl transition-all duration-300 group"
        >
          <LogOut size={18} className="group-hover:text-red-400 transition-colors" />
          <span className="font-medium text-sm group-hover:text-red-400 transition-colors">Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;